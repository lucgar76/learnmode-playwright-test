import socket
import uuid
import pytest
from kafka import KafkaProducer, KafkaConsumer, KafkaAdminClient, TopicPartition
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError

BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "test-learnmode"
CONSUMER_TIMEOUT_MS = 5000


def _broker_is_reachable() -> bool:
    try:
        with socket.create_connection(("localhost", 9092), timeout=1):
            return True
    except OSError:
        return False


pytestmark = pytest.mark.skipif(
    not _broker_is_reachable(),
    reason="Kafka is not running on localhost:9092",
)


def create_topic_if_missing():
    admin = KafkaAdminClient(bootstrap_servers=BOOTSTRAP_SERVERS)
    try:
        admin.create_topics([NewTopic(name=TOPIC, num_partitions=1, replication_factor=1)])
    except TopicAlreadyExistsError:
        pass
    finally:
        admin.close()


@pytest.fixture(scope="module", autouse=True)
def kafka_topic():
    create_topic_if_missing()


@pytest.fixture
def producer():
    p = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
    yield p
    p.close()


@pytest.fixture
def consumer():
    c = KafkaConsumer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        consumer_timeout_ms=CONSUMER_TIMEOUT_MS,
    )
    tp = TopicPartition(TOPIC, 0)
    c.assign([tp])
    end_offsets = c.end_offsets([tp])
    c.seek(tp, end_offsets[tp])
    yield c
    c.close()


@pytest.mark.kafka
class TestKafkaMessageBroker:

    def test_producer_connects_and_sends(self, producer):
        """Producer can connect to Kafka and send a message without errors."""
        future = producer.send(TOPIC, b"ping")
        record = future.get(timeout=10)
        assert record.topic == TOPIC
        assert record.partition >= 0
        assert record.offset >= 0

    def test_consumer_receives_message(self, producer, consumer):
        """A message sent by the producer is received by the consumer."""
        unique_payload = f"hello-{uuid.uuid4()}".encode()
        producer.send(TOPIC, unique_payload)
        producer.flush()

        received = [msg.value for msg in consumer]
        assert unique_payload in received, (
            f"Expected message '{unique_payload}' not found in received messages: {received}"
        )

    def test_message_content_is_preserved(self, producer, consumer):
        """The message content received matches exactly what was sent."""
        payload = b"learnmode-kafka-validation"
        producer.send(TOPIC, payload)
        producer.flush()

        received = [msg.value for msg in consumer]
        assert payload in received

    def test_multiple_messages_are_all_delivered(self, producer, consumer):
        """All messages sent in a batch are received by the consumer."""
        messages = [f"msg-{i}-{uuid.uuid4()}".encode() for i in range(5)]
        for msg in messages:
            producer.send(TOPIC, msg)
        producer.flush()

        received = [msg.value for msg in consumer]
        for expected in messages:
            assert expected in received, f"Message '{expected}' was not received"

    def test_message_order_is_preserved(self, producer, consumer):
        """Messages sent to the same partition arrive in order."""
        ordered_messages = [f"order-{i}".encode() for i in range(5)]
        for msg in ordered_messages:
            producer.send(TOPIC, msg)
        producer.flush()

        received = [msg.value for msg in consumer]
        filtered = [m for m in received if m.startswith(b"order-")]
        assert filtered == ordered_messages, (
            f"Expected order {ordered_messages} but got {filtered}"
        )

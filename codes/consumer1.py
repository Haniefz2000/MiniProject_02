import json 
from kafka import KafkaConsumer, KafkaProducer
import time
import logging
from datetime import datetime

print("Connecting to consumer to Add Timestamp...")
consumer = KafkaConsumer(
    'users_info',
    bootstrap_servers=['kafka-broker:29092'],
    auto_offset_reset='earliest',
    enable_auto_commit=False,  # Disable auto commit
    group_id='my-group',  # Dummy group id
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

producer = KafkaProducer(bootstrap_servers=['kafka-broker:29092'], max_block_ms=5000)

def add_timestamp(msg):
    data = msg.value
    data['timestamp'] = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    return data

def main():
    try:
        while True:
            # Poll for messages with a timeout of 1 second
            msg_batch = consumer.poll(timeout_ms=1000)
            if not msg_batch:
                break
            
            for tp, msgs in msg_batch.items():
                for msg in msgs:
                    new_msg = add_timestamp(msg)
                    producer.send('timestamp', json.dumps(new_msg).encode('utf-8'))
                    print(f"Added to: id: {new_msg['id']} Name: {new_msg['first_name']} {new_msg['last_name']} with Label: {new_msg['timestamp']} and sent to topic timestamp")
                    #print(msg.topic, msg.partition, msg.offset)
            
            # Manually commit the offsets of the processed messages
            consumer.commit()

    except KeyboardInterrupt:
        print("KeyboardInterrupt: Exiting...")
    except Exception as e:
        logging.error(f'An error occurred: {e}')
    finally:
        consumer.close()
        producer.flush()

if __name__ == '__main__':
    main()


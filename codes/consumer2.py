import json 
from kafka import KafkaConsumer, KafkaProducer
import time
import logging
from datetime import datetime
import random

print("Connecting to consumer to Add Label...")
consumer = KafkaConsumer(
    'timestamp',
    bootstrap_servers=['kafka-broker:29092'],
    auto_offset_reset='earliest',
    enable_auto_commit=False,  # Disable auto commit
    group_id='my-group',  # Dummy group id
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

producer = KafkaProducer(bootstrap_servers=['kafka-broker:29092'], max_block_ms=5000)

def add_labels(msg):
    data = msg.value
    data['label'] = random.choice(['A', 'B', 'C'])
    return data

def main():
    try:
        while True:
            msg_batch = consumer.poll(timeout_ms=1000)  # Poll for messages with 1 second timeout
            if not msg_batch:  # If no messages received, break out of loop
                break
            
            for tp, msgs in msg_batch.items():
                for msg in msgs:
                    new_msg = add_labels(msg)
                    producer.send('label', json.dumps(new_msg).encode('utf-8'))
                    print(f"Label added to: id: {new_msg['id']} Name: {new_msg['first_name']} {new_msg['last_name']} with Label: {new_msg['label']} and sent to topic label")
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


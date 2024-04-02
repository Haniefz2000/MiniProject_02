import json 
from kafka import KafkaConsumer
import time
import logging
import psycopg2


print("Connecting to consumer to read from kafka and send to postgresql db....")
consumer = KafkaConsumer(
    'label',
    bootstrap_servers=['kafka-broker:29092'],
    auto_offset_reset='earliest',
    enable_auto_commit=False,  # Disable auto commit
    group_id='my-group',  # Dummy group id
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)


def main():
	# Connect to PostgreSQL
	conn = psycopg2.connect(
	    dbname="dblab",
	    user="postgres",
	    password="postgres123",
	    host="postgres",
	    port="5432"
	)
	cur = conn.cursor()
	# Create the users table if it doesn't exist
	cur.execute("""
	    CREATE TABLE IF NOT EXISTS users (
		id VARCHAR(255) PRIMARY KEY,
		first_name VARCHAR(255),
		last_name VARCHAR(255),
		gender VARCHAR(255),
		address VARCHAR(255),
		post_code VARCHAR(255),
		email VARCHAR(255),
		username VARCHAR(255),
		dob VARCHAR(255),
		registered_date VARCHAR(255),
		phone VARCHAR(255),
		picture VARCHAR(255),
		timestamp VARCHAR(255),
		label VARCHAR(255)
	    )
	""")
	conn.commit()
	try:
		while True:
			msg_batch = consumer.poll(timeout_ms=1000)  # Poll for messages with 1 second timeout
			if not msg_batch:  # If no messages received, break out of loop
				break

			for tp, msgs in msg_batch.items():
				for msg in msgs:
					
					data= {}
					data = msg.value
					#attributes = list(data.keys())
					#['id', 'first_name', 'last_name', 'gender', 'address', 'post_code', 'email', 'username', 'dob', 'registered_date', 'phone', 'picture', 'timestamp', 'label']
					cur.execute("""INSERT INTO users (id, first_name, last_name, gender, address, post_code, email, username, dob, registered_date, phone, picture, timestamp, label) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (data['id'], data['first_name'] , data['last_name'], data['gender'], data['address'] , data['post_code'], data['email'] , data['username'] , data['dob'], data['registered_date'] , data['phone'] , data['picture'] , data['timestamp'], data['label'] ))
			    		#print(msg.topic, msg.partition, msg.offset)
			conn.commit()

			# Manually commit the offsets of the processed messages
			consumer.commit()

	except KeyboardInterrupt:
		print("KeyboardInterrupt: Exiting...")
	except Exception as e:
		logging.error(f'An error occurred: {e}')
	finally:
		consumer.close()
		cur.close()
    	#conn.close()

if __name__ == '__main__':
    main()


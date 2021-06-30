### 参考代码

```python
# -*- coding: utf-8 -*-
"""
Subject: 消费指定时间窗内所产生的消息
@Author YH YR
@Time 2019/01/23 21:23
"""
import time
from kafka import KafkaConsumer, TopicPartition


class ConsumerTimeStampWindow:
    def __init__(self, broker_list, group_name, topic, enable_auto_commit=True, auto_offset_reset='latest'):
        self.topic = topic
        self.consumer = KafkaConsumer(group_id=group_name, bootstrap_servers=broker_list,
                                      enable_auto_commit=enable_auto_commit, auto_offset_reset=auto_offset_reset)

    def consumer_from_offset_window(self, process_msg, begin_time, end_time):
        self.consumer.subscribe(self.topic)
        self.consumer.poll(0)

        begin_offset_dic, end_offset_dic = self.get_offset_time_window(begin_time, end_time)
        for topic_partition, offset_and_timestamp in begin_offset_dic.items():
            self.consumer.seek(topic_partition, offset_and_timestamp[0])

        topic_partition_info = self.consumer.assignment()
        partition_consumer_finish_flag = dict(zip(topic_partition_info, [False] * len(topic_partition_info)))

        while True:
            if False not in partition_consumer_finish_flag.values():
                return
            consumer_records = self.consumer.poll(100)
            for partition_info, records in consumer_records.items():
                if partition_consumer_finish_flag[partition_info]:
                    print('-------------- {0} consumer finish --------------'.format(partition_info))
                    break
                for record in records:
                    if record.offset <= end_offset_dic[partition_info][0]:
                        process_msg(record)
                    else:
                        partition_consumer_finish_flag[partition_info] = True

    def get_offset_time_window(self, begin_time, end_time):
        partitions_structs = []

        for partition_id in self.consumer.partitions_for_topic(self.topic):
            partitions_structs.append(TopicPartition(self.topic, partition_id))

        begin_search = {}
        for partition in partitions_structs:
            begin_search[partition] = begin_time if isinstance(begin_time, int) else self.__str_to_timestamp(begin_time)
        begin_offset = self.consumer.offsets_for_times(begin_search)

        end_search = {}
        for partition in partitions_structs:
            end_search[partition] = end_time if isinstance(end_time, int) else self.__str_to_timestamp(end_time)
        end_offset = self.consumer.offsets_for_times(end_search)

        for topic_partition, offset_and_timestamp in begin_offset.items():
            b_offset = 'null' if offset_and_timestamp is None else offset_and_timestamp[0]
            e_offset = 'null' if end_offset[topic_partition] is None else end_offset[topic_partition][0]
            print('Between {0} and {1}, {2} offset range = [{3}, {4}]'.format(begin_time, end_time, topic_partition,
                                                                              b_offset, e_offset))
        return begin_offset, end_offset

    @staticmethod
    def __str_to_timestamp(str_time, format_type='%Y-%m-%d %H:%M:%S'):
        time_array = time.strptime(str_time, format_type)
        return int(time.mktime(time_array)) * 1000


def print_msg(msg_dic):
    print(msg_dic)


if __name__ == '__main__':
    broker_list = 'localhost:9092'
    group_name = 'group_test'
    topic = 'topic_demo'

    action = ConsumerTimeStampWindow(broker_list, group_name, topic)
    action.consumer_from_offset_window(print_msg, '2019-01-23 21:30:00', '2019-01-23 21:36:00')
```


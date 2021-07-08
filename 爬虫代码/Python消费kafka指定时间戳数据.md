### 参考代码

```python
'''
Author: herongwei
Date: 2021-06-30 20:36:59
LastEditTime: 2021-07-08 16:52:16
LastEditors: Please set LastEditors
Description: 消费指定时间窗内所产生的消息(注意)
offsets_for_times：按时间戳查找给定分区的偏移量。 每个分区返回的偏移量是对应分区中时间戳大于或等于给定时间戳的最早偏移量。
FilePath: /spider/bin/fk_offset.py
'''
import base64
import codecs
import chardet
import time
import json
from kafka import KafkaConsumer, TopicPartition

count = 0
class ConsumerTimeStampWindow:
    def __init__(self, bs_server, group_name, topic, enable_auto_commit, auto_offset_reset, all_partition):
        self.topic = topic
        self.all_partition = all_partition
        self.consumer = KafkaConsumer(group_id=group_name, bootstrap_servers=bs_server,
                                    enable_auto_commit=enable_auto_commit,auto_offset_reset=auto_offset_reset)
    
    def comsumer_from_offset_between_window(self, process_msg, begin_time, end_time):
        #self.consumer.subscribe(self.topic)
        #self.consumer.assign([TopicPartition(self.topic, 0)])
        all_partition_dic = []
        for i in range(self.all_partition):
            all_partition_dic.append(TopicPartition(topic=self.topic, partition=i))
        self.consumer.assign(all_partition_dic)    
        #self.consumer.poll(0)
        #调用 get_offset_time_window 返回开始和结束时间偏移
        #对每一个分区进行seek
        # all_partition_dic = []
        # for i in range(self.all_partition):
        #     all_partition_dic.append(TopicPartition(topic=self.topic, partition=i+1))
        
        begin_offset_dic, end_offset_dic = self.get_offset_time_window(begin_time, end_time)
        for topic_partition, offset_and_timestamp in begin_offset_dic.items():
            #print("begin_topic_partition==",topic_partition, offset_and_timestamp)
            #不知道为什么还有 None 类型
            if offset_and_timestamp is not None:
                self.consumer.seek(topic_partition, offset_and_timestamp[0])
        #for topic_partition, offset_and_timestamp in end_offset_dic.items():
            #print("end_topic_partition==",topic_partition, offset_and_timestamp)
        #获取当前分配给此使用者的分区集。
        topic_partition_info = self.consumer.assignment()
        partition_consumer_finish_flag = dict(zip(topic_partition_info, [False] * len(topic_partition_info)))

        while True:
            #全部消费完了更新为True？
            if False not in partition_consumer_finish_flag.values():
                return
            consumer_records = self.consumer.poll(100)
            for partition_info, records in consumer_records.items(): 
                #print("partition_info==========",partition_info)
                if partition_info and records:
                    if partition_consumer_finish_flag[partition_info]:
                        print('-------consumer finish---------{0}'.format(partition_info))
                        break
                    for record in records:
                        if end_offset_dic[partition_info] is not None:
                            if record.offset <= end_offset_dic[partition_info][0]:
                                process_msg(record)
                            else:
                                partition_consumer_finish_flag[partition_info] = True

		#按照开始和结束时间查询
    def comsumer_from_offset_begin_window(self, process_msg, begin_time, end_time):
        all_partition_dic = []
        for i in range(self.all_partition):
            all_partition_dic.append(TopicPartition(topic=self.topic, partition=i))
        self.consumer.assign(all_partition_dic)    
        #self.consumer.poll(0)
        #调用 get_offset_time_window 返回开始和结束时间偏移
        #对每一个分区进行seek
        
        begin_offset_dic, end_offset_dic, max_end_offset = self.get_offset_time_window(begin_time, end_time)
        for topic_partition, offset_and_timestamp in begin_offset_dic.items():
            if offset_and_timestamp is not None:
                self.consumer.seek(topic_partition, offset_and_timestamp[0])
        #获取当前分配给此使用者的分区集。
        topic_partition_info = self.consumer.assignment()
        partition_consumer_finish_flag = dict(zip(topic_partition_info, [False] * len(topic_partition_info)))

        while True:
            #全部消费完了更新为True？
            if False not in partition_consumer_finish_flag.values():
                return
            consumer_records = self.consumer.poll(100)
            for partition_info, records in consumer_records.items(): 
                if partition_info and records:
                    if partition_consumer_finish_flag[partition_info]:
                        print('-------consumer finish---------{0}'.format(partition_info))
                        break
                    for record in records:
                        if record.offset <= max_end_offset:
                            #print("end_offset_time=========", record.offset,max_end_offset)
                            process_msg(record)
                        else:
                            partition_consumer_finish_flag[partition_info] = True
    
    def get_offset_time_window(self, begin_time, end_time):
        partitions_structs = []
        #consumer.assign([
        #    TopicPartition(topic=my_topic, partition=0),
        #    TopicPartition(topic=my_topic, partition=1)])
        #获取该 topic 下面所有的 partitions
        for partitions_id in self.consumer.partitions_for_topic(self.topic):
            partitions_structs.append(TopicPartition(self.topic,partitions_id))
        
        #   主要是调用 offsets_for_times 接口 对每个分区进行时间戳偏移
        #   入参：字典：分区ID+时间戳
        #   出参：items 字典  TopicPartition:OffsetAndTimestamp
        begin_search = {}
        for partition in partitions_structs:
            begin_search[partition] = begin_time if isinstance(begin_time, int) else self.__str_to_timestamp(begin_time)
            #print("begin_offset_dic=====",partition, begin_search[partition])
        begin_offset = self.consumer.offsets_for_times(begin_search)

        end_search = {}
        max_end_offset = 0
        for partition in partitions_structs:
            end_search[partition] = end_time if isinstance(end_time, int) else self.__str_to_timestamp(end_time)
            #print("end_offset_dic=====",partition, end_search[partition])
        end_offset = self.consumer.offsets_for_times(end_search)

        #for topic_partition, offset_and_timestamp in begin_offset.items():
            #print("begin_topic_partition==",topic_partition, offset_and_timestamp)
            #不知道为什么还有 None 类型
        for topic_partition, offset_and_timestamp in end_offset.items():
            if offset_and_timestamp is not None:
                if offset_and_timestamp[0] > max_end_offset:
                    max_end_offset = offset_and_timestamp[0]
                    #print("end_topic_partition==",topic_partition, offset_and_timestamp, type(offset_and_timestamp[0]))

        # for topic_partition, offset_and_timestamp in begin_offset.items():
        #     b_offset = 'null' if offset_and_timestamp is None else offset_and_timestamp[0]
        #     e_offset = 'null' if end_offset[topic_partition] is None else end_offset[topic_partition][0]
            #print('Between {0} and {1}, {2} offset range = [{3}, {4}]'.format(begin_time, end_time, topic_partition,b_offset, e_offset))
        return begin_offset, end_offset, max_end_offset
    
    @staticmethod
    def __str_to_timestamp(str_time, format_type='%Y-%m-%d %H:%M:%S'):
        time_array = time.strptime(str_time, format_type)
        return int(time.mktime(time_array)) * 1000

def print_msg(msg_dic):
    global count
    msg_val = json.loads(msg_dic.value.decode("utf-8"))
    response = msg_val["response"]
    url = msg_val["request"]["url"]
    # if response["status"][1] == 200:
    #     body = base64.b64decode(response["body"])# base64 decode body
    #     encoding = chardet.detect(body)["encoding"]
    #     body_vivo = body.decode(encoding)# 如果要消费前100条数据直接加切片[:100]
    count += 1
    print("body_url=",url,count)
    
if __name__ == '__main__':
    bs_server = "xxxx"
    group_name = 'test'
    topic = "xxxid" # 指定需要消费的主题
    #auto_offset_reset = 'latest'
    auto_offset_reset = 'earliest'
    begin_time = '2021-07-08 00:00:00'
    end_time   = '2021-07-08 00:00:00'
    all_partition = 30 # 所有分区
    action = ConsumerTimeStampWindow(bs_server, group_name, topic, True, auto_offset_reset, all_partition)
    action.comsumer_from_offset_begin_window(print_msg, begin_time, end_time)
```


#!/usr/bin/env python3
'''Task 12 Improved: Nginx Log Stats with Top 10 IPs.'''
from pymongo import MongoClient


def print_nginx_request_logs(nginx_collection):
    '''Prints stats about Nginx request logs and top 10 IPs.'''
    # Total number of logs
    log_count = nginx_collection.count_documents({})
    print(f'{log_count} logs')

    # Methods count
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    print('Methods:')
    for method in methods:
        method_count = nginx_collection.count_documents({'method': method})
        print(f'\tmethod {method}: {method_count}')

    # Status check count
    status_check_count = nginx_collection.count_documents({'method': 'GET', 'path': '/status'})
    print(f'{status_check_count} status check')

    # Top 10 IPs
    print('IPs:')
    top_ips = nginx_collection.aggregate([
        {'$group': {'_id': '$ip', 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}},
        {'$limit': 10}
    ])

    for ip in top_ips:
        print(f'\t{ip["_id"]}: {ip["count"]}')

def run():
    '''Provides some stats about Nginx logs stored in MongoDB.'''
    client = MongoClient('mongodb://127.0.0.1:27017')
    print_nginx_request_logs(client.logs.nginx)

if __name__ == '__main__':
    run()

#!/usr/bin/env python3
'''task14
'''


def top_students(mongo_collection):
    '''Returns all students sorted by average score.'''
    students = mongo_collection.aggregate([
        {
            '$project': {
                'name': 1,
                'topics': 1,
                'averageScore': { '$avg': '$topics.score' }
            }
        },
        {
            '$sort': { 'averageScore': -1 }
        }
    ])
    return list(students)

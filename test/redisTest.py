import redis
import json
import pickle

def main():
    r=redis.StrictRedis(host='localhost', port=6379, db='mydb')
    r.set('fruit','orange')
    print(r.get('fruit'))
    emp_dict={}
    emp_dict['101'] = {'empid':101,'name':'Alan','designation':'developer'}
    r.set('101', pickle.dumps(emp_dict))
    redis_data = pickle.loads(r.get('101'))

    print(redis_data)

if __name__ == '__main__':
    main()
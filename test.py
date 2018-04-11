import multiprocessing

def worker(i):
    """worker function"""
    print 'Worker' + str(i)
    return

if __name__ == '__main__':
    jobs = []
    for i in range(5):
        p = multiprocessing.Process(target=worker(i))
        jobs.append(p)
        p.start()
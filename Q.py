Q = []

def enqueue(video_id):
    Q.append(video_id)
    print(Q)

def dequeue():
    return Q.pop(0)

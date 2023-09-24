Q = []

def enqueue(video_id):
    Q.append(video_id)

def dequeue():
    return Q.pop(0)

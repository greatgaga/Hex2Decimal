import pyopencl as cl
import numpy as np
import hashlib

def crack_hash(hash):
    # init
    platform = cl.get_platforms()[0]
    device = platform.get_devices()[0]
    context = cl.Context([device])
    queue = cl.CommandQueue(context)

    # result buffer initialized to -1
    result_np = np.array([-1], dtype=np.int32)
    result_buf = cl.Buffer(context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=result_np)

    # passwords
    password_list = []

    # reading passwords from wordlist
    with open("wordlist.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            password_list.append(line.strip())
    # formating passwords for further use

    password_list = [p.ljust(8, '\x00')[:8] for p in password_list]  # pad or truncate to 8 bytes
    flat_candidates = b''.join(p.encode('utf-8') for p in password_list)
    candidates_np = np.frombuffer(flat_candidates, dtype=np.uint8)
    candidates_buf = cl.Buffer(context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=candidates_np)

    # target hash (SHA-1)
    #target_password = "12345678"
    #target_hash = hashlib.sha1(target_password.encode()).digest()
    if len(hash) != 40:
        print("Error: Hash should be a 40-character SHA-1 hex string.")
        return
    target_hash = bytes.fromhex(hash)
    target_hash_np = np.frombuffer(target_hash, dtype=np.uint8)
    target_hash_buf = cl.Buffer(context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=target_hash_np)

    # compile the kernel
    with open("sha1_crack.cl", "r") as f:
        kernel_source = f.read()

    program = cl.Program(context, kernel_source).build()
    kernel = program.sha1_kernel

    # set kernel args ONCE
    kernel.set_args(candidates_buf, target_hash_buf, result_buf)

    # launch the kernel once over N candidates
    global_size = (len(password_list),)
    cl.enqueue_nd_range_kernel(queue, kernel, global_size, None)

    # read result
    cl.enqueue_copy(queue, result_np, result_buf)
    queue.finish()

    # print result
    if result_np[0] != -1:
        print("Hash cracked, password is: ", password_list[result_np[0]])
    else:
        print("Hash not cracked.\nTry another wordlist.")

    result_np[0] = -1
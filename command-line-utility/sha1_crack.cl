__kernel void sha1_kernel(__global const char* candidates,
                          __global const uchar* target_hash,
                          __global int* result_index)
{
    int idx = get_global_id(0);
    // Exit if a match has already been found.
    if (result_index[0] != -1) return;

    // Load 8-byte password into two 32-bit words (big-endian).
    int base = idx * 8;
    uint W[80];
    W[0] = ((uint)((uchar)candidates[base+0]) << 24) |
           ((uint)((uchar)candidates[base+1]) << 16) |
           ((uint)((uchar)candidates[base+2]) <<  8) |
           ((uint)((uchar)candidates[base+3]));
    W[1] = ((uint)((uchar)candidates[base+4]) << 24) |
           ((uint)((uchar)candidates[base+5]) << 16) |
           ((uint)((uchar)candidates[base+6]) <<  8) |
           ((uint)((uchar)candidates[base+7]));
    // Append 0x80 bit and pad zeros.
    W[2] = 0x80000000;
    for(int i = 3; i < 14; i++) {
        W[i] = 0x00000000;
    }
    // Length in bits (64) in last word.
    W[14] = 0x00000000;
    W[15] = 8 * 8;  // 8 bytes * 8 = 64 bits


    // Message schedule expansion.
    for(int i = 16; i < 80; i++) {
        uint tmp = W[i-3] ^ W[i-8] ^ W[i-14] ^ W[i-16];
        W[i] = (tmp << 1) | (tmp >> 31);
    }

    // Initialize SHA-1 state.
    uint a = 0x67452301;
    uint b = 0xEFCDAB89;
    uint c = 0x98BADCFE;
    uint d = 0x10325476;
    uint e = 0xC3D2E1F0;

    // 80-round compression.
    for(int i = 0; i < 80; i++) {
        uint f, K;
        if (i < 20) {
            f = (b & c) | ((~b) & d);
            K = 0x5A827999;
        } else if (i < 40) {
            f = b ^ c ^ d;
            K = 0x6ED9EBA1;
        } else if (i < 60) {
            f = (b & c) ^ (b & d) ^ (c & d);
            K = 0x8F1BBCDC;
        } else {
            f = b ^ c ^ d;
            K = 0xCA62C1D6;
        }
        uint temp = ((a << 5) | (a >> 27)) + f + e + K + W[i];
        e = d;
        d = c;
        c = (b << 30) | (b >> 2);
        b = a;
        a = temp;
    }
    // Compute final hash values by adding to initial state.
    uint h0 = a + 0x67452301;
    uint h1 = b + 0xEFCDAB89;
    uint h2 = c + 0x98BADCFE;
    uint h3 = d + 0x10325476;
    uint h4 = e + 0xC3D2E1F0;

    // Build 32-bit words from target hash bytes.
    uint t0 = ((uint)target_hash[0] << 24) | ((uint)target_hash[1] << 16)
            | ((uint)target_hash[2] <<  8) |  (uint)target_hash[3];
    uint t1 = ((uint)target_hash[4] << 24) | ((uint)target_hash[5] << 16)
            | ((uint)target_hash[6] <<  8) |  (uint)target_hash[7];
    uint t2 = ((uint)target_hash[8] << 24) | ((uint)target_hash[9] << 16)
            | ((uint)target_hash[10] <<  8) | (uint)target_hash[11];
    uint t3 = ((uint)target_hash[12] << 24) | ((uint)target_hash[13] << 16)
            | ((uint)target_hash[14] <<  8) | (uint)target_hash[15];
    uint t4 = ((uint)target_hash[16] << 24) | ((uint)target_hash[17] << 16)
            | ((uint)target_hash[18] <<  8) | (uint)target_hash[19];

    // If hash matches target, write the index.
    if (h0 == t0 && h1 == t1 && h2 == t2 && h3 == t3 && h4 == t4) {
        atomic_cmpxchg(result_index, -1, idx);
    }
}

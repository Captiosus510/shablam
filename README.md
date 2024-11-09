Project idea: Shablam

What it does
Shazam but for videos
Upload pictures (major scenes from movies?) (or short video clips?) to find their source

How it works
Video fingerprinting?
Idk how this works on a more specific level

Why we are doing this
Convenience: want to watch a movie from a clip you see online but you don’t know where it’s from
Higher application
Plagiarism? 

Plan
Pick a fingerprinting method 
Hashing methods: dHash - compare differences between neighbouring pixels with imagehash python library
Input image, store in db
Make database - use SQLite - has built in hamming distance integration
Smth smth machine learning
Input movie, takes key frames
Key frames are fingerprinted, compared with hamming distance

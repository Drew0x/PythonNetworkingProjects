[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/WpFrneSV)
# Overview

The goal of this project assignment is to assess your understanding of how to build a distributed application using indirect communication, with paradigms such as producer-consumer and publish-subscribe.

# Bitcoin Mining

Cryptocurrency is a type of digital currency that uses cryptography to regulate its creation and secure fund transfers. Bitcoin, introduced in 2009, was the first widely adopted cryptocurrency, designed to enable direct peer-to-peer transactions. Each Bitcoin transaction is recorded and verified on a decentralized, distributed, and publicly accessible digital ledger known as the blockchain.

How Bitcoin Transaction Authentication Works

* Initiation: A user initiates a transaction by agreeing to send a digital asset (e.g., Bitcoin) to another user.
* Broadcast: The transaction is broadcast to the Bitcoin peer-to-peer network, where it awaits verification by nodes.
* Block Formation: Verified transactions are grouped together into a structure called a block.
* Hash Creation: A unique hash is generated for the block using its transaction data, the hash of the previous block, and a random number called a **nonce**.
* Mining: Specialized nodes called miners compete to find a valid **nonce** that solves a complex mathematical puzzle. The first miner to solve it earns the right to add the block to the blockchain and receives a reward.

The **nonce** in a block is a 32-bit number that is adjusted so the resulting hash of the block contains a specific number of leading zeros. These leading zeros determine the difficulty level of the mining process: the more leading zeros required, the fewer valid hashes exist, making the problem harder to solve.

Blockchain security relies on the fact that each block verifies the integrity of all previous blocks. Therefore, altering a single block would require modifying all subsequent blocks as well. As a result, the security of previously mined blocks increases with each new block added to the chain.

Bitcoin mining pools allow miners to combine their computational resources and share their hashing power. Rewards are distributed proportionally based on each miner’s contribution to solving a block. In contrast, solo miners work independently and typically use a process called **bitcoind**, a background service (daemon) that helps retrieve information about new transactions from the Bitcoin network.

# Hashing 

A hash function maps data of arbitrary size to a fixed-size output, commonly referred to as a **digest** or hash value. Hash functions are valuable in cryptography because the **digest** can be used to verify whether the original data has been altered. A well-designed hash function makes it extremely difficult to reconstruct the original data from the hash value—that is, it is computationally hard to reverse the process. Examples of hash functions include MD5 and SHA-1. Specifically, MD5 produces a 128-bit hash value. The example in [src/hashing.py](src/hashing.py) demonstrates how to use MD5 in Python. The example demonstrates that even a small change in the input for MD5 produces a completely different hash value.  

# Instructions

In this project, you are asked to simulate the process of Bitcoin mining using Python and the STOMP communication protocol. The suggested architecture for the simulation uses two topic queues named: **/topic/bitcoin/tasks** and **/topic/bitcoin/solutions**. 

## The Main Process

A **bitcoin task** is represented using a Python dictionary and it has two parts: 

* data: a sequence of 32 bytes;
* zeros: an integer number that specifies the number of leading zeros.

For example: 

```
 {
    'data': [119, 99, 109, 110, 104, 102, 108, 113, 102, 118, 122, 116, 121, 111, 119, 108, 105, 99, 109, 102, 100, 112, 102, 102, 108, 110, 98, 101, 117, 101, 97, 106], 
    'zeros': 8
 }
```

The main process will publish tasks to the miner processes using a dedicated topic queue named **/topic/bitcoin/tasks**. To simplify implementation, assume that the required number of leading zeros is always a multiple of eight. A task is considered solved when a nonce is found such that the hash **digest** of the task's data, combined with the computed **nonce**, contains the specified number of leading zeros.

The main process subscribes to a topic queue named **/topic/bitcoin/solutions**, which is used by the miner processes to broadcast when a solution for a task is found. A **bitcoin solution** is represented using a Python dictionary and it has two parts: 

* task: the task dictionary;
* nonce: the nonce that solved the task.

When a solution is announced, the main process should extract the task reported by the miner process and save the found **nonce** into an output file. Then, if there are more tasks in the backlog, the main process should generate and publish another task.

## The Miner Process

A miner process receives a notification whenever a new task is published to the **/topic/bitcoin/tasks** topic queue. Upon finding a solution, the miner immediately reports it to all processes via the **/topic/bitcoin/solutions** topic queue. If a miner receives a notification that the task it is currently working on has already been solved, it should stop processing that task immediately.

## File Formats 

The input file contains an arbitrary number of tasks, one per line. Each task consists of two parts separated by a comma: a sequence of bytes (the data portion) and the required number of leading zeros, which is always a multiple of eight. Use the provided [data/input.txt](data/input.txt) file to test your program. The output file, [data/output.txt](data/output.txt), mirrors the input format but includes an additional field—the **nonce** value found—represented as a sequence of four bytes. All fields are comma-separated.

# Rubric

```
+20 mine function
+15 tasks listener 
+15 solutions listener 
+10 solutions listener setup 
+10 tasks listener setup 
+10 tasks are published by the main process
+5 code is thread-safe
+10 any task with zeros <=3 are solved in less than 1m 
+5 output with solutions is generated and clears bitcoin test
```
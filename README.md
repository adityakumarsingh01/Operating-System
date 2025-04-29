## Multithreading Models Simulator

**Multithreading Models Simulator** is a Python-based GUI project that visually demonstrates how different thread management models and synchronization mechanisms work in operating systems. It is designed to help students and developers understand key concepts of thread scheduling, kernel-user thread mapping, and safe access to shared resources using semaphores and monitors.

---

### **Project Objective**

To simulate and visualize core multithreading models (Many-to-One, One-to-Many, Many-to-Many) and synchronization techniques (Semaphore, Monitor) in a way that is interactive, easy to understand, and educational for academic or practical learning purposes.

---

### **What This Project Demonstrates**

1. **Multithreading Models** :-
   - **Many-to-One** :-  
     ⦿ Multiple user-level threads map to a single kernel-level thread.  
     ⦿ Threads are executed one after another, simulating blocking behavior.  
   - **One-to-Many** :-  
     ⦿ Each user-level thread maps to a separate kernel-level thread.  
     ⦿ True concurrency can be observed as each thread executes independently.  
   - **Many-to-Many** :-  
     ⦿ Many user threads are mapped dynamically to a pool of kernel threads.  
     ⦿ A semaphore limits concurrent access, showing real-world CPU scheduling.  

2. **Thread Synchronization** :-  
   - **Semaphore-based Control** :-  
     ⦿ In the many-to-many model, semaphores ensure that only a limited number of threads can access kernel threads at once.  
   - **Monitor-based Resource Access** :-  
     ⦿ A `Condition` with a `Lock` simulates monitor-based synchronization where threads wait to access a shared resource one by one.  

---

### **Core Concepts Used**

- **Thread Creation & Management** using `threading.Thread`
- **Synchronization Mechanisms** :-  
  ⦿ `threading.Semaphore`  
  ⦿ `threading.Lock` and `threading.Condition` (Monitors)  
- **Visualization** with `Tkinter Canvas` :-  
  ⦿ Threads are shown as colored circles (running, waiting, finished)  
- **Logging System** :-  
  ⦿ Real-time logs of thread activities (start, execution, termination)  
  ⦿ Option to export logs to `.txt` files  

---

### **Features**

⦿ Visual simulation of different threading models  
⦿ Real-time thread execution logs  
⦿ User input for number of threads  
⦿ Save execution logs to file  
⦿ Lightweight GUI designed for 14-inch screens  
⦿ Educational tool for Operating Systems labs projects  

---

### **Technologies Used**

- **Python 3.8+**
- **Tkinter** – for GUI development
- **Python threading module** – for multithreading and synchronization
- **Semaphores & Locks** – for thread control and safety

---

### **Use Cases**

- 🎓 OS lab simulations
- 📘 Learning multithreading and synchronization in Python
- 📊 Visual aid for academic presentations and vivas

---

This project not only simulates thread execution, but also serves as a **visual teaching tool** for understanding how operating systems handle multiple threads using different models and techniques.

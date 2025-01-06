import heapq

class CRMHeap:
    def __init__(self):
        self.heap = []

    def add_request(self, priority, customer):
        heapq.heappush(self.heap, (priority, customer))  

    def process_request(self):
        if self.heap:
            priority, customer = heapq.heappop(self.heap)  
            print(f"Processing request: {customer} with priority {priority}")
        else:
            print("No requests to process.")

    def display_requests(self):
        if self.heap:
            print("Current Requests in Heap (Priority Queue):")
            for priority, customer in self.heap:
                print(f"Priority: {priority}, Customer: {customer}")
        else:
            print("No requests in the queue.")


# Example
crm_heap = CRMHeap()
crm_heap.add_request(3, "Customer1:Daniel")
crm_heap.add_request(1, "Customer2: Patrick")  
crm_heap.add_request(5, "Customer3: Allan")

crm_heap.display_requests()
crm_heap.process_request()  # Process the highest priority
crm_heap.display_requests()




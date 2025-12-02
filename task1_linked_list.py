class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, value):
        new_node = Node(value)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.value)
            current = current.next
        return result

    # Reverse linked list
    def reverse(self):
        prev = None
        current = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    @staticmethod
    def _merge_sorted_lists(l1: Node, l2: Node) -> Node:
        if not l1:
            return l2
        if not l2:
            return l1

        if l1.value < l2.value:
            head = l1
            l1 = l1.next
        else:
            head = l2
            l2 = l2.next

        tail = head

        while l1 and l2:
            if l1.value < l2.value:
                tail.next = l1
                l1 = l1.next
            else:
                tail.next = l2
                l2 = l2.next
            tail = tail.next

        tail.next = l1 if l1 else l2
        return head

    # Merge sort
    def merge_sort(self):
        def sort(head: Node) -> Node:
            if not head or not head.next:
                return head

            slow, fast = head, head.next
            while fast and fast.next:
                slow = slow.next
                fast = fast.next.next

            mid = slow.next
            slow.next = None

            left = sort(head)
            right = sort(mid)

            return LinkedList._merge_sorted_lists(left, right)

        self.head = sort(self.head)

    @classmethod
    def merge_sorted(cls, list1, list2):
        merged_list = cls()
        merged_list.head = cls._merge_sorted_lists(list1.head, list2.head)
        return merged_list


if __name__ == "__main__":
    ll1 = LinkedList()
    ll2 = LinkedList()

    for v in [3, 1, 5, 7, 9, 0, 8]:
        ll1.append(v)

    for v in [4, 2, 6, 10, -1, 11, 5]:
        ll2.append(v)

    print("Original lists:")
    print(ll1.to_list())
    print(ll2.to_list())

    ll1.merge_sort()
    ll2.merge_sort()
    print("Sorted lists:")
    print(ll1.to_list())
    print(ll2.to_list())

    merged = LinkedList.merge_sorted(ll1, ll2)
    print("Merged list:")
    print(merged.to_list())

    merged.reverse()
    print("Reversed merged list:")
    print(merged.to_list())

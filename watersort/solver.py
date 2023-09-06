# Solver cho WaterSort sử dụng thuật toán DFS và A*

# Import numpy để xử lý array
# Import collections để có deque: hàng đợi 2 đầu
import numpy as np
from collections import deque, namedtuple


# Class WaterSort
class WaterSort:
    # Hàm khởi tạo: khởi tạo biến pos (position)
    # pos chỉ trạng thái hiện tại của bài toán
    def __init__(self, pos):
        self.pos = pos

    '''
    Function dùng để lấy giá trị khác 0 đầu tiên
    trong mảng
    '''

    @staticmethod
    def get_first_non_zero(arr):
        try:
            return arr[arr != 0][0]
        except IndexError:
            return 0

    """
    Lấy index của giá trị khác 0 đầu tiên
    np.nonzero nhận input là một mảng, lấy các giá trị khác 0
    và trả về index của chúng
    np.nonzero(arr)[0][0] trả về index của giá trị khác 0 đầu tiên
    (index của hàng)
    """

    @staticmethod
    def get_first_non_zero_index(arr):
        try:
            return np.nonzero(arr)[0][0]
        except IndexError:
            return 3

    '''
    Lấy index (hàng) của giá trị 0 cuối cùng của mảng
    '''

    @staticmethod
    def get_last_zero_index(arr):
        try:
            return np.where(arr == 0)[0][-1]
        except IndexError:
            return 3

    '''
    Tìm trạng thái có f nhỏ nhất trong danh sách (list)
    '''
    @staticmethod
    def findMin(li):
        minValue = 999
        minEle = -1
        for idx, element in enumerate(li):
            if element.f < minValue:
                minValue = element.f
                minEle = idx
        return minEle

    '''
    Tạo danh sách các move hợp lệ của trạng thái
    '''

    def get_legal_moves_list(self):
        move_to_list = np.where(self.pos[0] == 0)[0]  # Xét các bình chưa đầy
        first_non_zero_in_col = np.apply_along_axis(self.get_first_non_zero, 0, self.pos)  # Xét các bình có nước
        num_of_bottle = self.pos.shape[1]
        legal_move_list = tuple()  # Tạo danh sách move hợp lệ
        '''
        Xét từng bình chưa đầy:
        + Nếu bình trống --> xét các bình có thể đổ vào (bất kỳ giá trị khác 0)
        + Nếu không phải bình trống --> xét các bình có thể đổ vào
        (có giá trị == với bình đang xét), phải trừ bình đang xét ra
        Output: tuple gồm x và y với 
            x : array chứa danh sách các bình có thể đổ
            y : bình được đổ vào
        '''
        for bottle_no in move_to_list:
            if first_non_zero_in_col[bottle_no] == 0:
                legal_move_list += tuple([(np.where((first_non_zero_in_col != 0)
                                                    & (np.arange(num_of_bottle) != bottle_no))[0], bottle_no)])
            else:
                legal_move_list += tuple([(np.where((first_non_zero_in_col == first_non_zero_in_col[bottle_no])
                                                    & (np.arange(num_of_bottle) != bottle_no))[0], bottle_no)])
        return legal_move_list

    '''
    Nhận vào danh sách các move hợp lệ, chuyển thành danh sách
    trạng thái kế tiếp
    '''

    def state_create(self, legal_move_list):
        state_list = []
        for from_idx_list, to_idx in legal_move_list:
            for from_idx in from_idx_list:
                state = self.swap(from_idx, to_idx)
                state_list.append(state)

        return state_list

    '''
    Chuyển nước từ bình i sang bình j
    và cập nhật mảng mới đã được thay đổi
    '''

    def swap(self, i, j):
        next_state = self.pos.copy()
        '''
        Nhận vào 2 bình i và j
        Lấy phần tử khác 0 đầu tiên của bình j chuyển vào phần tử 0 cuối cùng của j
        '''
        idx_from = (self.get_first_non_zero_index(next_state[:, i]), i)
        idx_to = (self.get_last_zero_index(next_state[:, j]), j)

        x_from = idx_from[0]
        y_from = idx_from[1]
        x_to = idx_to[0]
        y_to = idx_to[1]
        '''
        Để có thể đổ lượng nước tối đa, ta có thể dùng vòng lặp while
        + Nếu node bên dưới node vừa bị swap có cùng màu
        + Nếu vẫn còn phần tử 0 bên bình được đổ vào
        --> Tiếp tục đổ
        '''
        swap_value = next_state[idx_from]
        while (next_state[idx_from] == swap_value) and (next_state[idx_to] == 0):
            next_state[idx_from], next_state[idx_to] = next_state[idx_to], next_state[idx_from]
            if (x_from < 3) and (x_to > 0):
                x_from += 1
                x_to -= 1
            idx_from = (x_from, y_from)  # Cập nhật idx_from và idx_to trước khi while lặp lại
            idx_to = (x_to, y_to)

        return WaterSort(next_state)  # Cập nhật trạng thái sau swap

    '''
    Hàm xác định mục tiêu của bài toán
    return true nếu tất cả hàng của trạng thái đều giống nhau
    '''

    def isgoal(self):
        return np.array_equiv(self.pos, self.pos[0])

    '''
    Sử dụng fronzenset để có thể đưa vào dictionary (hashable)
    '''

    def set_create(self):
        return frozenset(map(tuple, self.pos.T))

    '''
    Cho phep biểu diễn object của class ra thành giá trị đại diện có thể in được (str)
    '''

    def __repr__(self):
        return repr(self.pos)

    '''
    Cho phép lấy key của item thuộc Class waterSort
    '''

    def __getitem__(self, key):
        return self.pos[key]

    '''
    Function dùng để giải bài toán WaterSort theo Depth First Seach
    Ta tạo 1 stack để chứa các trạng thái chưa duyệt
    Tạo 1 dictionary tên "path" để lưu parent của 1 state
    Tạo 1 deque ( hoặc có thể là queue ) để lưu solution sau khi đã tìm xong kết quả
    '''

    def solveDFS(pos):
        # Tạo các hàng chờ:
        stack = deque([pos])  # Stack chứa trạng thái hiện tại
        path = {pos.set_create(): None}  # Dictionary chứa danh sách các bước trạng thái
        solution = deque()  # Hàng chờ sẽ được dùng để chứa các bước tới kết quả

        while not pos.isgoal():
            next_move_list = pos.get_legal_moves_list()  # Tạo danh sách các move hơp lệ
            next_state_list = pos.state_create(next_move_list)  # Tạo danh sách các trạng thái kế tiếp
            for state in next_state_list:  # Xét từng trạng thái vưa tạo
                if state.set_create() in path:  # Nếu state đã xuất hiện -> skip
                    continue
                path[state.set_create()] = pos  # Lưu pos thành parent của state
                stack.append(state)  # Đưa state vào stack
            if stack:
                pos = stack.pop()  # Pop stack và dùng phần tử vừa pop làm pos để tiếp tục sinh state
            else:
                print("Unsolvable")
                return -1

        while pos:
            solution.appendleft(pos)  # đưa từng bước vào solution
            pos = path[pos.set_create()]  # Truy xuất đến "node" cha của bước hiện tại đã lưu trong path

        if solution is not None:
            return list(solution)
        else:
            return -1

    '''
    Function dùng để tính heuristic cho trạng thái
    + Xuất phát từ 0, mỗi khi trong 1 bình có màu trùng từ 2 đến 3 node, ta trừ
    điểm tương ứng
    + Nếu có cột đã đầy + cùng màu ta trừ 5 điểm
    '''
    @staticmethod
    def heuristic(curr_state):
        curr = np.array(list(curr_state))
        point = 0
        trans_arr = curr.T                      # Chuyển vị ma trận để dễ dàng xử lý theo hàng
        for i in range(trans_arr.shape[0]):
            if np.all(trans_arr[i] == trans_arr[i][0]):     # Nếu tất cả phần tử 1 hàng giống nhau --> Bình đầy cùng màu
                point -= 5
            else:
                unique, counts = np.unique(trans_arr[i], return_counts=True)
                list_unique = np.asarray((unique, counts)).T
                for j in range(list_unique.shape[0]):
                    if (list_unique[j][0] > 0) and (list_unique[j][1] > 1):
                        point -= list_unique[j][1]

        return point

    '''
    Function giải bải toán WaterSort bằng giải thuật A*
    Tạo một danh sách open list chứa các trạng thái chưa duyệt 
    Đối với mỗi trạng thái, lưu f, g, h với:
        f = g + h
        g = cost
        h = heuristic
    Với mỗi bước duyệt, ta chọn trạng thái có f nhỏ nhất trong list
    '''
    def solveAStar(pos):
        state_detail = namedtuple('State', ['state', 'f', 'g', 'h'])    # Dùng namedtuple để có thể lưu f, g, h
        open_list = []                          # Khởi tạo open list
        path = {pos.set_create(): None}         # Dictionary chứa danh sách các bước trạng thái
        solution = deque()                      # Hàng chờ sẽ được dùng để chứa các bước tới kết quả
        found_goal = False                      # Nếu tìm thấy state kết quả --> True

        start_state = state_detail(pos, 0, 0, 0)    # Trạng thái khởi đầu sẽ có f = 0
        open_list.append(start_state)

        while len(open_list) > 0 and found_goal == False:
            min_f_state = pos.findMin(open_list)                    # Tìm trạng thái có f nhỏ nhất
            pos = open_list.pop(min_f_state)[0]                     # Chuyên thành trạng thái hiện tại
            next_move_list = pos.get_legal_moves_list()             # Tạo danh sách move hợp lệ
            next_state_list = pos.state_create(next_move_list)      # Tạo danh sách trạng thái kế tiếp
            for state in next_state_list:
                if state.set_create() in path:
                    continue
                path[state.set_create()] = pos
                if state.isgoal():
                    pos = state
                    found_goal = True
                    break
                # Cost được tính theo mỗi bước = 1
                # Để tính bước ta dùng dictionary path để truy xuất từng state đến khi gặp None
                state_g = 0
                state_temp = state
                while state:
                    state_g -= 1
                    state = path[state.set_create()]
                # Heuristic
                state = state_temp
                state_h = pos.heuristic(state)
                # Đưa trạng thái vào open list:
                state_desc = state_detail(state, state_g + state_h, state_g, state_h)
                open_list.append(state_desc)

        if not found_goal:
            print("Unsolvable")
            return -1

        while pos:
            solution.appendleft(pos)        # đưa từng bước vào solution
            pos = path[pos.set_create()]    # Truy xuất đến "node" cha của bước hiện tại đã lưu trong path

        if solution is not None:
            return list(solution)
        else:
            return -1

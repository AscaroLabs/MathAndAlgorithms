class Permutation:

	###################################################################
	# 
	# Способы инициализации перестановки:
	# -> Полная таблица в формате {1:i[1]; 2:i[2]; ... ; n:i[n]}
	# -> Через значения (аргументами являются 1, 2, ... , n) 
	#    (i[1], i[2], ... , i[n])
	# -> В виде цикла (рекомендуется указывать n - число эл-в 
	#    множества)
	# 
	# 
	# 		Поля 
	# 
	# self.table = dict()			# Табличное педставление
	# self.chain = list()			# Вторая строка табличного 
	# 								  представления
	# self.cycle = list()			# Представление в виде цикла
	# self.n = int()				# Мощность множеста элементов 
	# 
	# 
	# 		Методы
	# 
	# show(self, only_table: bool = None) -> None
	# Выводит информацию о перестановке в стандартный поток вывода
	# 
	# __init__(
	# 		self, 
	# 		table: dict = None, 
	# 		chain: list[int] = None, 
	# 		cycle = None, 
	# 		n: int = None
	# 	) -> None:
	# Конструктор
	# 
	# __mul__(self, other: "Permutation") -> "Permutation"
	# Умножение перестановок
	# 
	# __pow__(self, other: int) -> "Permutation"
	# Возведение перестановок в натуральную степень
	# 
	# __eq__(self, other: "Permutation") -> bool
	# Проверка равенства двух перестановок
	# 
	# order(self) -> int
	# Определение порядка перестановки
	# 
	# sort_by_index(self) -> "Permutation"
	# Сортурует перестановку по верхней строчке (создает копию)
	# 		
	# sign(self) -> int
	# Вычисляет знак (четность) перестановки
	# 
	# cycling(self) -> list[list[int]]
	# Представляет перестановку в виде произведения
	# независимых циклов
	#
	# 
	# 	Статические
	# 
	# cycle_to_table(cycle: list[int], n: int = None) -> dict
	# Метод преобразует перестановку в виде цикла в табличный вид 
	# 
	# identity_element(n: int = None,
	# 				   table: "Permutation" = None) -> "Permutation":	 
	# Метод определяет нейтральную перестановку определенного размера
	# 
	# 
	###################################################################
	
	
	@staticmethod
	def cycle_to_table(cycle: list[int], n: int = None) -> dict:
		if isinstance(cycle[0], int):
			if n is None:
				n = max(cycle)
			elif n < max(cycle):
				raise IndexError('Max element in '\
								 'cycle is {}, n = {}'.format(max(cycle), n))
			table = {}
			for i in range(1, n + 1):					
				if i in cycle:
					index_ = cycle.index(i)
					if index_ != len(cycle) - 1:
						table[i] = cycle[index_ + 1]
					else:
						table[i] = cycle[0]
				else:
					table[i] = i
			return(table)
		max_n = 1
		for c in cycle:
			if max_n < max(c):
				max_n = max(c)
		if n is None:
			n = max_n
		elif n < max_n:
			raise IndexError('Max element in '\
							 'cycle is {}, n = {}'.format(max_n, n))

		permutation_ = Permutation.identity_element(n=n)

		for c in cycle[::-1]:
			permutation_ = Permutation(cycle=c, n=n) * permutation_

		return permutation_.table


	@staticmethod
	def identity_element(n: int = None,
						 table: "Permutation" = None) -> "Permutation":
		if n is not None:
			t = dict()
			for i in range(1, n + 1):
				t[i] = i
			return Permutation(table=t)



	def show(self, only_table: bool = None) -> None:
		if only_table:
			for key in self.table.keys():
				print(key, end='\t')
			print()
			for value in self.table.values():
				print(value, end='\t')
			print('\n','\n')
			return
		print("Табличное представление")
		print("-----------------------")
		for key in self.table.keys():
			print(key, end='\t')
		print()
		for value in self.table.values():
			print(value, end='\t')
		print()
		print("Циклическое представление")
		print("-------------------------")
		for c in self.cycle:
			print('(', end=' ')
			for i in c:
				print(i, end=' ')
			print(")", end=' ')
		print()


	def __init__(
			self, 
			table: dict = None, 
			chain: list[int] = None, 
			cycle = None, 
			n: int = None
		) -> None:

		if table is not None:
			self.cycle = cycle
			self.table = table
			self.chain = list(self.table.values())
			self.n = len(self.table)
			self.cycle = self.cycling()
		elif chain is not None:
			self.chain = chain
			self.cycle = cycle
			self.table = {}
			for key, value in enumerate(self.chain):
				self.table[key + 1] = value
			self.n = len(self.table)
			self.cycle = self.cycling()
		elif cycle is not None:
			self.cycle = cycle
			if n is None:
				self.table = self.cycle_to_table(cycle=self.cycle)
				self.n = max(list(self.table.keys()) + list(self.table.values()))
			else:
				self.n = n
				self.table = self.cycle_to_table(cycle=self.cycle, n=self.n)
			self.chain = list(self.table.values())
		else:
			raise TypeError('Not enough arguments')


	def __mul__(self, other: "Permutation") -> "Permutation":
		p1 = self.table
		p2 = other.table
		p = dict()
		for i in range(1, len(p1) + 1):
			p[i] = p1[p2[i]]
		return Permutation(table=p)


	def __pow__(self, other: int) -> "Permutation":
		power = int(other)
		p = Permutation(table=self.table)
		ans = p
		for i in range(power - 1):
			ans *= p
		return ans


	def __eq__(self, other: "Permutation") -> bool:
		if self.n != other.n:
			return False
		n = self.n
		for i in range(1, n + 1):
			if self.table[i] != other.table[i]:
				return False
		return True


	def order(self) -> int:
		q = 1
		t = Permutation(table=self.table)
		n = self.n
		while True:
			if t ** q == Permutation.identity_element(n):
				return q
			else:
				q += 1


	def sort_by_index(self) -> "Permutation":
		t = self.table
		t = dict(sorted(t.items()))
		return Permutation(table=t)


	def inverse(self):
		t = dict()
		for i, n in self.table.items():
			t[n] = i
		return Permutation(table=t).sort_by_index()


	def sign(self) -> int:
		length_of_cycles = 0
		for c in self.cycle:
			length_of_cycles += sum(c)
		return (-1) ** (length_of_cycles - len(self.cycle))


	def cycling(self) -> list[list[int]]:
		if self.cycle is not None:
			return self.cycle
		orbits = list()
		for i in self.table.keys():
			contain = False
			for orbit in orbits:
				if i in orbit:
					contain = True
					break
			if contain:
				continue
			current = i
			orbits.append([])
			orbits[-1].append(current)
			current = self.table[current]
			while current != i:
				orbits[-1].append(current)
				current = self.table[current]
		return orbits

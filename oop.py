import copy
import csv
import sys


import functools
import tkinter as TK
from tkinter import ttk as TTK
from tkinter.filedialog import askopenfilename
from tkinter import messagebox, Button
import os


class Size():
    def __init__(self,row = 0, col = 0):
        self.__row = row
        self.__col = col
    def getRow(self):
        return self.__row
    def getCol(self):
        return self.__col
    def setRow(self,new_row):
        self.__row = new_row
    def setCol(self, new_col):
        self.__col = new_col

# class Web(enum.Enum):
#     Phishing = 1
#     Not_Phishing = 0

class split_file():
    def __init__(self,filename):
        minus_one, one = 0, 0
        try:
            with open(filename) as file: #naiveBayes.csv phishing.csv
                table = csv.reader(file, delimiter=' ')
                for line in table:
                    separator_line = line[0].split(',')
                    line_without_index_col = separator_line[1:] #[1:] for phishing
                    if line_without_index_col[-1] == '-1':
                        minus_one += 1
                    elif line_without_index_col[-1] == '1':
                        one += 1
            print("The total dataset size {}.\nThe legit dataset size {} and phishing dataset size {}.".format(minus_one+one,minus_one, one))
        except Exception as e:
            print("We have an error with your file, please check it again.")
        self.minus_one = minus_one
        self.one = one

    def get_split_file(self):
        return  self.minus_one, self.one

class  table_size():
    def __init__(self,rows,cols,table,dataset_name):
        minus_one,one = 0,0
        self.table = table
        for row in range(rows):
            if table[row][cols-1] == '-1':
                minus_one += 1
            elif table[row][cols-1] == '1':
                one += 1
        self.line = "The {} dataset contains {} legit samples and {} phishing samples .".format(dataset_name,minus_one,one)
        self.minus_one=minus_one
        self.one=one

    def get_table_size(self):
        return self.line, self.minus_one, self.one

class openfile():
    def __init__(self,filename):
        self.filename = filename
        split_data=split_file(self.filename)
        self.minus_one, self.one = split_data.get_split_file()
        self.test_data, test_data_a, test_data_b ,self.train_data = [], [], [], []
        counter_b,counter_a,self.rows_number ,self.col_number,index ,header= 0,0,0,0,0,0
        answer = TK.messagebox .askyesno(title='confirmation',
                          message='Do you have header in the table ?')
        if answer:
            delete_header = 'Y'
        else:
            delete_header = 'N'
        # delete_header = str(input("Do you have header in the table ?  Y/N\n"))

        answer = TK.messagebox .askyesno(title='confirmation',
                          message='Do you have Index column ?')
        if answer:
            delete_index_col = 'Y'
        else:
            delete_index_col = 'N'
        # delete_index_col = str(input("Do you have Index column ?  Y/N\n"))

        if delete_index_col == 'Y':
            index = 1
        else:
            index = 0
        if delete_header == 'Y':
            header = 1
        else:
            header = 0
        #try:

        with open(self.filename) as file:  # naiveBayes.csv phishing.csv
                table = csv.reader(file, delimiter=' ')
                for lines in table:
                    self.rows_number += 1
                    separator_line = lines[0].split(',')
                    self.col_number = len(separator_line)
                    line_without_index_col = separator_line[index:]
                    if line_without_index_col[-1] == '-1' and counter_a < (self.minus_one * 0.3):
                        test_data_a.append(line_without_index_col)
                        counter_a += 1
                    elif line_without_index_col[-1] == '1' and counter_b < (self.one * 0.3):
                        test_data_b.append(line_without_index_col)
                        counter_b += 1
                    elif not (separator_line[0][0].isalpha()):
                        self.train_data.append(line_without_index_col)  # insert to phishing table
        self.test_data = test_data_a + test_data_b
        #except Exception as e:
            #print("We have an error with your file, please check it again.\n")
        #finally:
        self.train_data = self.train_data [header:] #without the table header
    def get_open_file(self):
           return (self.rows_number, self.col_number, self.train_data, self.test_data)

class class_prob():
    def __init__(self,rows,cols, train_data):
        self.one, self.minus_one, self.prob_class_one,\
        self.prob_class_minus_one=0,0,0,0
        for row in range(rows):
            cell_value = train_data[row][cols-1]
            if cell_value == '1':
                self.one += 1
            elif cell_value == '-1':
                self.minus_one += 1
            else:
                print("cell value is unexpected :",cell_value)
        self.prob_class_one = self.one / rows
        self.prob_class_minus_one = self.minus_one / rows
        self.get_class_prob()
    def get_class_prob(self):
         return self.one, self.minus_one, self.prob_class_one, self.prob_class_minus_one

class laplacian_correction():
        def __init__(self, class_list,prob_values_given_class):
            self.corrected = copy.deepcopy(prob_values_given_class)
            laplacian = sum(class_list) + (len(prob_values_given_class))
            for value in range(len(self.corrected)):
                if self.corrected[value] in [0.0, 0]:
                    self.corrected[value] = 1 / laplacian
                else:
                    self.corrected[value] = (class_list[value] + 1 )/ laplacian
        def get_laplacian_correction(self):
                return self.corrected

class items_set():
    def __init__(self,rows, cols,prob_table):
        temp_list,set_table = [],[0] * (cols)
        self.set_dict = {}
        for col in range(cols):
            for row in range(rows):
                 temp_list.append(prob_table[row][col])
            set_table[col] = len(set(temp_list))
            self.set_dict.update({col : len(set(temp_list))})
            temp_list = []
        self.max_set = max(set_table)
    def get_items_set(self):
        return self.set_dict,self.max_set

class attr_prob():
    def __init__(self,dict, rows, cols, prob_table, class_one, class_minus_one):
        item_set = items_set(rows, cols, prob_table)
        self.set_dict,num = item_set.get_items_set()
        self.prob_dict = dict
        for col in range(cols):
            one_class_list, minus_one_class_list ,temp_list0 ,temp_list1 = [0] * num, [0] * num, [0] * num, [0] * num
            for row in range(rows):
                cell_value = prob_table[row][col]
                if cell_value == '1':
                    if prob_table[row][cols-1] == '1':  #yes - phishing
                        one_class_list[1] += 1
                    elif prob_table[row][cols-1] == '-1':  #no - legit
                        minus_one_class_list[1] += 1
                elif cell_value == '-1':
                    if prob_table[row][cols-1] == '1':
                        one_class_list[2] += 1
                    elif prob_table[row][cols-1] == '-1':
                        minus_one_class_list[2] += 1
                elif cell_value == '0':
                    if prob_table[row][cols-1] == '1':
                        one_class_list[0] += 1
                    elif prob_table[row][cols-1] == '-1':
                        minus_one_class_list[0] += 1
                else:
                    print("cell value is unexpected :", cell_value)
            # one_class_list.index(0) != set_dict.get(col)
            temp_list1=[0]*self.set_dict.get(col)
            final_value, final_values = 0,0
            for final_values in range(self.set_dict.get(col)):
                temp_list1[final_values] = one_class_list[final_values]/class_one
            if 0 in temp_list1 and final_values == (self.set_dict.get(col)-1):
                laplace_for_one = laplacian_correction(one_class_list,temp_list1)
                temp_list1 = laplace_for_one.get_laplacian_correction()

            temp_list0 = [0] * self.set_dict.get(col)
            for final_value in range(self.set_dict.get(col)):
                temp_list0[final_value] = minus_one_class_list[final_value] / class_minus_one
            if 0 in temp_list0 and final_value == (self.set_dict.get(col)-1):
                laplace_for_minus_one = laplacian_correction(minus_one_class_list,temp_list0)
                temp_list0 = laplace_for_minus_one.get_laplacian_correction()

            self.prob_dict.update({col: [temp_list0,temp_list1]})
    def get_attr_prob(self):
        return self.prob_dict,self.set_dict

class reduce_list():
    def __init__(self, rows,cols,table,prob_dict,set_dict,prob_class_one,prob_class_minus_one):
        prob_table = table
        prob_x_given_class_one_list ,prob_x_given_class_minus_one_list = [0]*cols,[0]*cols
        prob_x_given_class_one, prob_x_given_class_minus_one,counter ,self.legit_counter_hit ,self.phishing_counter_hit= 0,0,0,0,0
        for row in range(rows):
            for col in range(cols): #for phishing
                    if prob_table[row][col] == '0':
                        prob_x_given_class_minus_one_list[col] = prob_dict.get(col)[0][0]
                        prob_x_given_class_one_list[col] = prob_dict.get(col)[1][0]
                    elif prob_table[row][col] == '1':
                        prob_x_given_class_minus_one_list[col] = prob_dict.get(col)[0][1]
                        prob_x_given_class_one_list[col] = prob_dict.get(col)[1][1]
                    elif prob_table[row][col] == '-1':
                        if set_dict.get(col) > 2:
                            prob_x_given_class_minus_one_list[col] = prob_dict.get(col)[0][2]
                            prob_x_given_class_one_list[col] = prob_dict.get(col)[1][2]
                        elif set_dict.get(col) == 2: #change the -1 index to 0 index
                            prob_x_given_class_minus_one_list[col] = prob_dict.get(col)[0][0]
                            prob_x_given_class_one_list[col] = prob_dict.get(col)[1][0]
                        else:
                            print("Error : You have a column attribute with one variable.")

            prob_x_given_class_one = functools.reduce(lambda x, y: x * y, prob_x_given_class_one_list, 1)
            prob_x_given_class_minus_one = functools.reduce(lambda x, y: x * y, prob_x_given_class_minus_one_list, 1)
            classifier_result = naive_bayes_classifier(prob_x_given_class_one, prob_class_one, prob_x_given_class_minus_one, prob_class_minus_one )
            legit, phishing = classifier_result.get_naive_bayes_classifier()
            if "Legit" in legit:
                if prob_table[row][cols-1] == '-1':
                    self.legit_counter_hit += 1
            elif "Phishing" in phishing:
                if prob_table[row][cols-1] == '1':
                    self.phishing_counter_hit += 1
    def get_reduce_list(self):
        return self.legit_counter_hit,self.phishing_counter_hit

class naive_bayes_classifier():
    def __init__(self,prob_x_given_class_one, prob_class_one, prob_x_given_class_minus_one, prob_class_minus_one):
        classifier = [0,0]
        self.legit, self.phishing=" "," "
        classifier[0] = prob_x_given_class_minus_one * prob_class_minus_one  # minus one
        classifier[1] = prob_x_given_class_one * prob_class_one
        #print('\n',classifier)
        # print("naive_bayes_classifier:", prob_x_given_class_one, prob_class_one, prob_x_given_class_minus_one, prob_class_minus_one)
        result = classifier.index(max(classifier))
        if result == 0:
            self.legit= "{}.".format("Legit")
        elif result == 1:
            self.phishing = "{}.".format("Phishing")
    def get_naive_bayes_classifier(self):
        return self.legit, self.phishing

class  final_porb():
    def __init__(self,sum_of_minus_one, sum_of_one, legit_counter_hit, phishing_counter_hit):
        self.print_legit,self.print_phishing = " "," "
        if sum_of_minus_one >= legit_counter_hit:
            self.print_legit = "\nThe dataset legit web accuracy percentage : {:.2f}".format(legit_counter_hit / sum_of_minus_one)
        else:
            self.print_legit = "\n Error : sum_of_minus_one < legit_counter_hit - Check the data ! "

        if sum_of_one >= phishing_counter_hit:
            self.print_phishing = "\nThe dataset phishing web accuracy percentage : {:.2f}".format(phishing_counter_hit / sum_of_one)
        else:
            self.print_phishing = "\n Error : sum_of_one < phishing_counter_hit - Check the data ! "
    def get_final_prob(self):
        return self.print_legit,self.print_phishing




def UpdateProgress(ProgressBar, Value):
    ProgressBar['value'] = Value
    root.update_idletasks()


def ExitCallBack():
    msg = messagebox.showinfo( "Exit", "Remember...\nPhishing is not just for fishermen")
    sys.exit(0)



if __name__ == '__main__':
    root = TK.Tk()
    root.geometry("300x100")
    root.title('Web phishing detector')
    progress = TTK.Progressbar(root, orient=TK.HORIZONTAL, length=300, mode='determinate')

    B = Button(root, text = "Exit", command = ExitCallBack)
    B.place(x = 150,y = 50)
    progress.pack()
    dirname = os.getcwd()
    dirname = TK.filedialog.askdirectory(initialdir=dirname, title='Select a Directory')
    if (dirname == ''):
        dirname = '/.'
    UpdateProgress(progress, 10)
    #root.title('Select ML data base file (.csv)')
    Names = askopenfilename(
        initialdir=dirname,
        filetypes=(("CSV Files", "*.csv"), ("EXCL Files", "*.xls*"), ("Text File", "*.txt"), ("All Files","*.*")),
        #title='Choose input file(s) or folder(s).'
    )

    if Names == '':
        sys.exit(-2)
    FileName = Names
    UpdateProgress(progress, 20)
    #root.title('please wait while building the classification model')
    UpdateProgress(progress, 40)
    train_dict , test_dict = {}, {}
    open_file = openfile('phishing.csv')
    row, col, train_data, test_data = open_file.get_open_file()
    #[print(i, sep='\n') for i in train_data]
    train = Size(len(train_data), len(train_data[1]) )
    print( "The training dataset is: {} X {} .".format(train.getRow(), train.getCol()))
    UpdateProgress(progress, 60)
    table_size_train = table_size(train.getRow(), train.getCol(), train_data, "train")
    print_size_train, sum_of_minus_one_trian,sum_of_one_trian = table_size_train.get_table_size()
    print(print_size_train)
    UpdateProgress(progress, 70)
    class_prob_train = class_prob(train.getRow(), train.getCol(), train_data)
    class_one ,class_minus_one ,prob_class_one ,prob_class_minus_one = class_prob_train.get_class_prob()
    attr_prob_train = attr_prob(train_dict, train.getRow(), train.getCol(), train_data, class_one, class_minus_one)
    train_dict, set_dict = attr_prob_train.get_attr_prob()
    reduce_list_train = reduce_list(train.getRow(), train.getCol(), train_data, train_dict, set_dict, prob_class_one, prob_class_minus_one)
    legit_counter_hit,phishing_counter_hit = reduce_list_train.get_reduce_list()
    final_porb_train =  final_porb(sum_of_minus_one_trian,sum_of_one_trian,legit_counter_hit,phishing_counter_hit)
    print_legit_trian,print_phishing_trian = final_porb_train.get_final_prob()
    print("\n\n***************** The training dataset results *****************")
    print(print_legit_trian, print_phishing_trian, sep='\n')
    test = Size(len(test_data), len(test_data[1]))
    print("\n\n***************** The test dataset results *****************")
    print("The test dataset is: {} X {} .".format(test.getRow(), test.getCol()))

    table_size_test = table_size(test.getRow(), test.getCol(), test_data,"test")
    print_size_test, sum_of_minus_one_test, sum_of_one_test = table_size_test.get_table_size()
    print(print_size_test)
    UpdateProgress(progress, 80)
    class_prob_test = class_prob(test.getRow(), test.getCol(),test_data)
    class_one, class_minus_one, prob_class_one, prob_class_minus_one = class_prob_test.get_class_prob()
    test_attr_prob = attr_prob(test_dict, test.getRow(), test.getCol(), test_data, class_one, class_minus_one)
    test_dict = test_attr_prob.get_attr_prob()
    test_reduce_list =reduce_list(test.getRow(), test.getCol(), test_data, train_dict, set_dict, prob_class_one, prob_class_minus_one)
    legit_counter, phishing_counter = test_reduce_list.get_reduce_list()
    test_final_prob =  final_porb(sum_of_minus_one_test, sum_of_one_test ,legit_counter, phishing_counter)
    print_legit_test, print_phishing_test = test_final_prob.get_final_prob()
    print(print_legit_test, print_phishing_test, sep='\n')
    UpdateProgress(progress, 90)
    UpdateProgress(progress, 100)
    root.mainloop()
    ExitCallBack()
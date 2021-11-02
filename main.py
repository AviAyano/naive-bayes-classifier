import copy
import csv
import enum
import functools
from enum import Enum
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

class Web(enum.Enum):
    Phishing = 1
    Not_Phishing = 0

def split_data():
    minus_one, one = 0, 0
    try:
        with open('phishing.csv') as file:
            table = csv.reader(file, delimiter=' ')
            for line in table:
                separator_line = line[0].split(',')
                line_without_index_col = separator_line[1:] #[1:] for phishing
                if line_without_index_col[-1] == '-1':
                    minus_one += 1
                elif line_without_index_col[-1] == '1':
                    one += 1
        print("The total dataset size {}.\nThe legit dataset size {} and phishing dataset size {}.".format(minus_one+one,minus_one, one))
        return(minus_one, one)
    except Exception as e:
        print("We have an error with your file, please check it again.\nPlease check it again.\n")

def table_size(rows,cols,prob_table,dataset_name):
    minus_one,one = 0,0
    table = prob_table
    for row in range(rows):
        if table[row][cols] == '-1':
            minus_one += 1
        elif table[row][cols] == '1':
            one += 1
    line = "The {} dataset contains {} legit samples and {} phishing samples .".format(dataset_name,minus_one,one)
    return(line,minus_one,one)

def openfile(minus_one,one):
    test_data, test_data_a, test_data_b ,prob_table = [],[], [], []
    counter_b,counter_a,rows_number ,col_number = 0,0,0,0
    try:
        with open('phishing.csv') as file: # naiveBayes.csv
            table = csv.reader(file, delimiter=' ')
            for lines in table:
                rows_number += 1
                separator_line = lines[0].split(',')
                line_without_index_col = separator_line[1:] #[1:] for phishing

                if line_without_index_col[-1] == '-1' and counter_a < (minus_one*0.3):
                    test_data_a.append(line_without_index_col)
                    counter_a +=1
                elif line_without_index_col[-1] == '1' and counter_b < (one*0.3):
                    test_data_b.append(line_without_index_col)
                    counter_b += 1
                elif not(separator_line[0][0].isalpha()):
                    prob_table.append(line_without_index_col)      #insert to phishing table
                line = ''.join(line_without_index_col)    #convert to string without a comma
                if len(line) > col_number and rows_number != 1:
                    col_number = len(line) - line.count('-') +1
        test_data = test_data_a + test_data_b
        #print("The test data is :",test_data,'\n',"The prob table is :",prob_table)
        return (rows_number-1,col_number,prob_table,test_data)
    except Exception as e:
        print("We have an error with your file, please check it again.\nPlease check it again.\n")
    finally:
        return(rows_number-1,col_number,prob_table,test_data)

    #[print(i,end=' ') for i in pishing_table[2] ]
                #print( line,'\n',col_number,'=',len(line) ,'-',line.count(',') ,'-',line.count('-'))
            #print(','.join(line))

def class_prob(rows,cols, prob_table):
    one, minus_one = 0,0
    for row in range(rows):
        cell_value = prob_table[row][cols]
        if cell_value == '1':
            one += 1
        elif cell_value == '-1':
            minus_one += 1
        elif cell_value == '0':
            minus_one += 1
        else:
            print("cell value is unexpected :",cell_value)
    prob_class_one = one / rows
    prob_class_minus_one = minus_one / rows
    #prob_class_zero = zero / rows
    #print("The class probability :","\nOne :",prob_class_one,"\nMinus_one :",prob_class_minus_one,"\nzero :",prob_class_zero)
    return (one,minus_one,prob_class_one,prob_class_minus_one)
    #print("Checking the probability rule equals to 1 :",prob_class_one+prob_class_minus_one+prob_class_zero)

def laplacian_correction( cols, class_list):
    corrected_list = copy.deepcopy(class_list)
    class_list = [int(i) for i in class_list]
    laplacian = sum(class_list) + (cols - 1)
    if 0 in corrected_list:
        for value in range(len(corrected_list)):
            if corrected_list[value] in [0.0, 0]:
                corrected_list[value] = 1 / laplacian
            else:
                corrected_list[value] = corrected_list[value] / laplacian
    return corrected_list

def item_set(rows, cols,prob_table):
    temp_list,set_table = [],[0] * (cols-1)
    for col in range(cols-1):
        for row in range(rows):
             temp_list.append(prob_table[row][col])
        set_table[col] = len(set(temp_list))
        temp_list = []
    max_set = max(set_table)
    #print("The item",max_set)
    return max_set

def attribute_prob(prob_dict, rows, cols, prob_table, class_one, class_minus_one):
    num= item_set(rows, cols, prob_table)
    for col in range(cols):
        one_class_list, minus_one_class_list ,temp_list0 ,temp_list1 = [0] * num, [0] * num, [0] * num, [0] * num
        for row in range(rows):
            prob_table[row] = laplacian_correction(cols, prob_table[row])
            cell_value = prob_table[row][col]
            if cell_value == '1':
                if prob_table[row][cols] == '1':  #yes - phishing
                    one_class_list[1] += 1
                elif prob_table[row][cols] == '-1':  #no - legit
                    minus_one_class_list[1] += 1
            elif cell_value == '-1':
                if prob_table[row][cols] == '1':
                    one_class_list[2] += 1
                elif prob_table[row][cols] == '-1':
                    minus_one_class_list[2] += 1
            elif cell_value == '0':
                if prob_table[row][cols] == '1':
                    one_class_list[0] += 1
                elif prob_table[row][cols] == '-1':
                    minus_one_class_list[0] += 1
            else:
                print("cell value is unexpected :", cell_value)
        for final_values in range(len(one_class_list)):
            temp_list1[final_values] = one_class_list[final_values]/class_one
        for final_value in range(len(minus_one_class_list)):
            temp_list0[final_value] = minus_one_class_list[final_value]/class_minus_one
        prob_dict.update({col: [temp_list0,temp_list1]})
    return prob_dict

    # #corrected_zero_list = laplacian_correction(rows, cols, class_zero_list)
    # corrected_one_list = laplacian_correction(rows, cols, prob_dict)
    # corrected_minus_one_list = laplacian_correction(rows, cols, prob_dict)

            # if phishing_table[row][30] == '0':
            #     if cell_value == '1':
            #         one_attribute += 1 # insert the class prob by attribute like under30 who buy..
            #         class_zero_list.insert(1, one_attribute / class_zero)
            #     elif cell_value == '-1':
            #         minus_one_attribute += 1
            #         class_zero_list.insert(2, minus_one_attribute / class_zero)
            #     elif cell_value == '0':
            #         zero_attribute += 1
            #         class_zero_list.insert(0, zero_attribute / class_zero)
            #     else:
            #         print("cell value is unexpected :", cell_value)
            #
            # elif phishing_table[row][30] == '1':
            #     if cell_value == '1':
            #         one_attribute += 1
            #         class_one_list.insert(1, one_attribute / class_one)
            #     elif cell_value == '-1':
            #         minus_one_attribute += 1
            #         class_one_list.insert(2, minus_one_attribute / class_one)
            #     elif cell_value == '0':
            #         zero_attribute += 1
            #         class_one_list.insert(0, zero_attribute / class_one)
            #     else:
            #         print("cell value is unexpected :", cell_value)
            #
            # elif phishing_table[row][30] == '-1':
            #     if cell_value == '1':
            #         one_attribute += 1
            #         class_minus_one_list.insert(1, one_attribute / class_minus_one)
            #     elif cell_value == '-1':
            #         minus_one_attribute += 1
            #         class_minus_one_list.insert(2, minus_one_attribute / class_minus_one)
            #     elif cell_value == '0':
            #         zero_attribute += 1
            #         class_minus_one_list.insert(0, zero_attribute / class_minus_one)
            #     else:
            #         print("cell value is unexpected :", cell_value)

            #print("attribute_prob", class_zero_list, class_one_list, class_minus_one_list)



    # class_zero_list = list(map(lambda x: x>0 , class_zero_list))
    # print("wooosdsddsoow",class_zero_list)
    # class_one_list = list(map(lambda x: x>0 , class_one_list))
    # class_minus_one_list = list(map(lambda x: x>0 , class_minus_one_list))

def reduce_lists(rows,cols,table,prob_dict,prob_class_one,prob_class_minus_one):
    prob_table = table
    prob_x_given_class_one_list ,prob_x_given_class_minus_one_list = [0]*cols,[0]*cols
    prob_x_given_class_one, prob_x_given_class_minus_one,counter ,legit_counter ,phishing_counter= 0,0,0,0,0
    for row in range(rows):

        for col in range(cols):
            if prob_table[row][cols] == '1':  # yes - phishing v[1]
                if prob_table[row][col] == '0':
                    prob_x_given_class_one_list[col] = prob_dict.get(col)[1][0]
                elif prob_table[row][col] == '1':
                    prob_x_given_class_one_list[col] = prob_dict.get(col)[1][1]
                elif prob_table[row][col] == '-1':
                    prob_x_given_class_one_list[col] = prob_dict.get(col)[1][2]
            elif prob_table[row][cols] == '-1':  # no - legit
                if prob_table[row][col] == '0':
                    prob_x_given_class_minus_one_list[col] = prob_dict.get(col)[0][0]
                elif prob_table[row][col] == '1':
                    prob_x_given_class_minus_one_list[col] = prob_dict.get(col)[0][1]
                elif prob_table[row][col] == '-1':
                    prob_x_given_class_minus_one_list[col] = prob_dict.get(col)[0][2]
        prob_x_given_class_one = functools.reduce(lambda x, y: x * y, prob_x_given_class_one_list, 1)
        prob_x_given_class_minus_one = functools.reduce(lambda x, y: x * y, prob_x_given_class_minus_one_list, 1)
        print("\nThe phishing website detector finds website number {} as: ".format(row),end='')
        result = naive_bayes_classifier(prob_x_given_class_one, prob_class_one, prob_x_given_class_minus_one, prob_class_minus_one )
        print(result,end=" ")
        if "Legit" in result:
            legit_counter += 1
            print(legit_counter)
        else:
            phishing_counter += 1
            print(phishing_counter)

    return (legit_counter,phishing_counter)
    # #print("reduce_lists",corrected_zero_list, corrected_one_list, corrected_minus_one_list)
    #prob_x_given_class_zero = functools.reduce(lambda x,y: x*y, corrected_zero_list,1)
    #prob_x_given_class_one = functools.reduce(lambda x,y: x*y, corrected_one_list ,1)
    #prob_x_given_class_minus_one = functools.reduce(lambda x,y: x*y, corrected_minus_one_list,1)
    # #print("\nThe class probability:\n", corrected_zero_list, '\n', corrected_one_list, '\n', corrected_minus_one_list)
    # #print("wooooow",prob_x_given_class_zero,prob_x_given_class_one,prob_x_given_class_minus_one)
    # #naive_bayes_classifier(prob_x_given_class_zero, class_zero, prob_x_given_class_one, class_one, prob_x_given_class_minus_one,class_minus_one)


    #print("The website is : "+str(row), "\nOne :", prob_class_one, "\nMinus_one :", prob_class_minus_one, "\nZero :",prob_class_zero)

def naive_bayes_classifier(prob_x_given_class_one, prob_class_one, prob_x_given_class_minus_one, prob_class_minus_one):
    classifier = [0,0]
    #classifier[0] = prob_x_given_class_z * class_z
    classifier[0] = prob_x_given_class_minus_one * prob_class_minus_one  # minus one
    classifier[1] = prob_x_given_class_one * prob_class_one
    #print('\n',classifier)
    #print("naive_bayes_classifier:", prob_x_given_class_one, prob_class_one, prob_x_given_class_minus_one, prob_class_minus_one)
    result = classifier.index(max(classifier))
    if result == 0:
        return "{}.".format("Legit")
    elif result == 1:
        return "{}.".format("Phishing")
    else:
        return "{}.".format("Unknown")

def final_porb(sum_of_minus_one,sum_of_one,legit_counter,phishing_counter):
    print_legit,print_phishing = " "," "
    if sum_of_minus_one > legit_counter:
        print_legit = "\nThe dataset legit web accuracy percentage : {:.2f}".format(legit_counter / sum_of_minus_one)
    else:
        print_legit = "\nThe dataset legit web accuracy percentage : {:.2f} \nstandard deviation is : {:.2f}".format(legit_counter / sum_of_minus_one , (legit_counter - sum_of_minus_one)/ sum_of_minus_one)

    if sum_of_one > phishing_counter:
        print_phishing = "\nThe dataset phishing web accuracy percentage : {:.2f}".format(phishing_counter / sum_of_one)
    else:
        print_phishing = "\nThe dataset phishing web accuracy percentage : {:.2f} \nstandard deviation is : {:.2f}".format(phishing_counter / sum_of_one , (phishing_counter - sum_of_one)/ sum_of_one)
    return print_legit,print_phishing
if __name__ == '__main__':
    prob_dict ,test_dict = {}, {}
    minus_one, one = split_data()
    row, col, prob_table,test_data = openfile(minus_one,one)
    prob_table = prob_table [1:] #for phishing without header
    train = Size( len(prob_table),len(prob_table[1])-1)
    test = Size(len(test_data),len(test_data[1])-1)
    print( "The training dataset is: {} X {} \nThe test dataset is: {} X {}".format(train.getRow(), train.getCol() ,test.getRow(),test.getCol()))
    print_size, sum_of_minus_one,sum_of_one = table_size(train.getRow(), train.getCol(), prob_table,"train")
    print(print_size)
    #[print(i,sep='\n') for i in phishing_table ]
    class_one ,class_minus_one ,prob_class_one ,prob_class_minus_one = class_prob(train.getRow(),train.getCol(), prob_table)
    prob_dict = attribute_prob(prob_dict, train.getRow(), train.getCol(), prob_table, class_one, class_minus_one)
    legit_counter,phishing_counter = reduce_lists(train.getRow(),train.getCol(),prob_table,prob_dict,prob_class_one,prob_class_minus_one)
    #print(Web.Phishing.name)
    print_legit_trian,print_phishing_trian = final_porb(sum_of_minus_one,sum_of_one,legit_counter,phishing_counter)






    print("The test dataset is: {} X {} ".format(test.getRow(), test.getCol()))
    #test_data = test_data[1:]
    print_size, sum_of_minus_one, sum_of_one = table_size(test.getRow(), test.getCol(), test_data,"test")
    print(print_size)
    class_one, class_minus_one, prob_class_one, prob_class_minus_one = class_prob(test.getRow(), test.getCol(),test_data)
    test_dict = attribute_prob(test_dict, test.getRow(), test.getCol(), test_data, class_one, class_minus_one)
    legit_counter, phishing_counter = reduce_lists(test.getRow(),test.getCol(),test_data,test_dict,prob_class_one,prob_class_minus_one)
    print_legit_test, print_phishing_test = final_porb(sum_of_minus_one, sum_of_one, legit_counter, phishing_counter)

    print("\n***************** The training dataset results *****************")
    print(print_legit_trian, print_phishing_trian, sep='\n')
    print("\n***************** The test dataset results *****************")
    print(print_legit_test, print_phishing_test, sep='\n')
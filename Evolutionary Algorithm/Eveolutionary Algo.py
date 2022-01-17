import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image
import matplotlib.image as img


image = img.imread('groupGray.jpg')
boothi = img.imread('boothiGray.jpg')
rows, columns = image.shape
pop_size = 100


def initialization_population(rows, columns,pop_size):
    random_points1 = np.random.randint(rows, size=pop_size)
    random_points2 = np.random.randint(columns, size=pop_size)
    a_zip = list(zip(random_points1,random_points2))
    return a_zip


def fitness_evaluation(image, boothi,random_points):
    rows = []
    columns = []
    fitness=[]
    for x,y in random_points:
        rows.append(x)
        columns.append(y)
    for i in range(len(random_points)):
        if rows[i] + 35 < 512 and columns[i] + 29 < 1024:
            num = image[rows[i]:rows[i]+35,columns[i]:columns[i]+29]    
            co_relation = np.corrcoef(boothi.ravel(),num.ravel())
            fitness.append(co_relation[0,1])
        else:
            fitness.append(-1)
    return fitness


def Selection(random_points,fitness):
    Ranked_Pop = []
    Ranked_Pop = list(zip(random_points,fitness))
    Ranked_Pop.sort(key=lambda x:x[1],reverse=True)
    Rand_points = []
    Fitness = []
    
    for x,y in Ranked_Pop:
        Rand_points.append(x)
        Fitness.append(y)
    return Rand_points, Ranked_Pop
    
    
def Cross_Over(Rand_points):
    a = []
    b = []
    a_bin = []
    b_bin = []
    for x,y in Rand_points:
        a.append(x)
        b.append(y) 
    for i in range(len(a)):
        
        a_bin.append(bin(a[i])[2:].zfill(9))
        b_bin.append(bin(b[i])[2:].zfill(10))
    A_list =[]
    for i in range(len(a_bin)):
        A_list.append(a_bin[i] + b_bin[i])
    New_generation = []
    for i in range(0,len(A_list),2):
            
        slicer = np.random.randint(0,18)
        left1 = A_list[i]
        left_left = left1[:slicer]
        left_right = left1[slicer:]
        left2 = A_list[i+1]
        left2_left = left2[:slicer]
        left2_right = left2[slicer:]
        temp1 = left_left + left2_right
        temp2 = left2_left + left_right
        left_temp1 = temp1[:9]
        right_temp1 = temp1[9:]
        
        left_temp1 = int(left_temp1,2)
        right_temp1 = int(right_temp1,2)
        New_generation.append((left_temp1,right_temp1))
        left_temp2 = temp2[:9]
        right_temp2 = temp2[9:]
        left_temp2 = int(left_temp2,2)
        right_temp2 = int(right_temp2,2)
        New_generation.append((left_temp2,right_temp2))
    return New_generation


def Mutation(Evolved_Pop):
    a = []
    b = []
    a_bin = []
    b_bin = []
    for x,y in Evolved_Pop:
        a.append(x)
        b.append(y)   
    for i in range(len(a)):
        
        a_bin.append(bin(a[i])[2:].zfill(9))
        b_bin.append(bin(b[i])[2:].zfill(10))
    A_list =[]
    new_list = []
    for i in range(len(a_bin)):
        A_list.append(a_bin[i] + b_bin[i])
    for i in range(len(A_list)): 
        random = np.random.randint(0,19)
        Check = list(A_list[i])
        if Check[random] == '0':
            Check[random] = '1'
            temp1 = Check
            temp1 = ''.join([str(elem) for elem in temp1])
            left_temp1 = temp1[:9]
            right_temp1 = temp1[9:]
            left_temp1 = int(left_temp1,2)
            right_temp1 = int(right_temp1,2)
            new_list.append((left_temp1,right_temp1))
        elif Check[random] == '1':
            Check[random] = '0'
            temp2 = Check
            temp2 = ''.join([str(elem) for elem in temp2])
            left_temp2 = temp2[:9]
            right_temp2 = temp2[9:]
            
            left_temp2 = int(left_temp2,2)
            right_temp2 = int(right_temp2,2)
            new_list.append((left_temp2,right_temp2))
    return new_list  
            

Population = initialization_population(rows, columns,pop_size)
fitness = fitness_evaluation(image, boothi,Population)
mean = []
maax = []
for i in range(5000):
    # print(i)
    Ranked_Population, Ranked_Pop = Selection(Population,fitness)
    Average = sum(fitness) / len(fitness)
    mean.append(Average)
    gen = i
    Max = Ranked_Pop[0][1]
    maax.append(Max)
    Evolved_Pop = Cross_Over(Ranked_Population)
    Population = Mutation(Evolved_Pop)
    fitness= fitness_evaluation(image, boothi,Population)
    msg = False
    for i in range(len(fitness)):
        if fitness[i] > 0.8:
            print ('sucesss ')
            num3 = i
            msg = True
    if msg is True:
        break
# print(mean)
# print(maax)
print(gen)
print(Population[num3])
y,x=Population[num3]
plt.plot(maax)
font1 = {'family':'serif','color':'blue','size':15}
font2 = {'family':'serif','color':'darkred','size':15}
# plt.title("Crossover and Mutation with 5000 pop size", fontdict = font1)
plt.xlabel("Generations", fontdict = font2)
plt.ylabel("Average of fitness",fontdict = font2)
plt.plot(mean)
plt.show()

image=Image.open('groupGray.jpg')
gray_image=image.convert('L')
gray_image_array=np.asarray(gray_image)
plt.imshow(gray_image_array,cmap='gray', vmin = 0, vmax = 255)
plt.gca().add_patch(Rectangle((x,y),29,35,linewidth=1,edgecolor='r',facecolor='none'))

plt.show()

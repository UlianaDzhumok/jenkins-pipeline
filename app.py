# Imports python modules
from time import time, sleep

# Imports python modules to work with directories
from os import listdir, path
import argparse

#Imports libriaries to work with CNN models
import ast
from PIL import Image
import torchvision.transforms as transforms
from torch.autograd import Variable
import torchvision.models as models
from torch import __version__

def get_input_args():
    
    parser = argparse.ArgumentParser()

    parser.add_argument('--dir', type = str, default = 'pet_images/', 
                    help = 'path to the folder of pet images') 
    
    return parser.parse_args()

def check_command_line_arguments(in_arg):

    if in_arg is None:
        print("* Doesn't Check the Command Line Arguments because 'get_input_args' hasn't been defined.")
    else:
        # prints command line agrs
        print("\nCommand Line Arguments:\n     dir =", in_arg.dir)

def check_creating_pet_image_labels(results_dic):

    if results_dic is None:
        print("\n* Doesn't Check the Results Dictionary because 'get_pet_labels' hasn't been defined.\n")
    else:
        # Code to print 10 key-value pairs (or fewer if less than 10 images)
        # & makes sure there are 40 pairs, one for each file in pet_images/
        stop_point = len(results_dic)
        if stop_point > 10:
            stop_point = 10
        print("\nPet Image Label Dictionary has", len(results_dic),
              "key-value pairs.\nBelow are", stop_point, "of them:")
    
        # counter - to count how many labels have been printed
        n = 0
    
        # for loop to iterate through the dictionary
        for key in results_dic:
 
            # prints only first 10 labels
            if n < stop_point:
                print("{:2d} key: {:>30}  label: {:>26}".format(n+1, key,
                      results_dic[key][0]) )

                # Increments counter
                n += 1
            
            # If past first 10 (or fewer) labels the breaks out of loop
            else:
                break

def get_pet_labels(image_dir):

    filename_list = listdir(image_dir)
    results_dic={}
    
    for i in range(0, len(filename_list), 1):
        if not filename_list[i].startswith("."):
            
            if filename_list[i] not in results_dic:
                pet_name=""
                filename_words=path.splitext(filename_list[i])[0].split("_")

                for word in filename_words:
                    if word.isalpha():
                        pet_name += word + " "
                results_dic[filename_list[i]] = [pet_name.lower().strip()]
            else:
                print("** Warning: Key=", filename_list[i], 
               "already exists in results_dict with value =", 
                results_dic[filename_list[i]])
    
    return results_dic

def classify_images(images_dir, results_dic):
    
    for filename, pet_image_label in results_dic.items():
        classifier_label = classifier(images_dir+filename).lower().strip()
        result=[pet_image_label[0], classifier_label]
        
        if pet_image_label[0] in classifier_label:
            result.append(1)
        else:
            result.append(0)

        results_dic[filename]=result

def classifier(img_path):
    
    # obtain ImageNet labels
    with open('imagenet1000_clsid_to_human.txt') as imagenet_classes_file:
        imagenet_classes_dict = ast.literal_eval(imagenet_classes_file.read())

    
    # load the image
    img_pil = Image.open(img_path)

    # define transforms
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # preprocess the image
    img_tensor = preprocess(img_pil)
    
    # resize the tensor (add dimension for batch)
    img_tensor.unsqueeze_(0)
    
    pytorch_ver = __version__.split('.')
    
    # pytorch versions 0.4 & hihger - Variable depreciated so that it returns
    # a tensor. So to address tensor as output (not wrapper) and to mimic the 
    # affect of setting volatile = True (because we are using pretrained models
    # for inference) we can set requires_gradient to False. Here we just set 
    # requires_grad_ to False on our tensor 
    if int(pytorch_ver[0]) > 0 or int(pytorch_ver[1]) >= 4:
        img_tensor.requires_grad_(False)
    
    # pytorch versions less than 0.4 - uses Variable because not-depreciated
    else:
        # apply model to input
        # wrap input in variable
        data = Variable(img_tensor, volatile = True) 

    # apply model to input
    model = models.vgg16(pretrained=True)
    
    # puts model in evaluation mode
    # instead of (default)training mode
    model = model.eval()
    
    # apply data to model - adjusted based upon version to account for 
    # operating on a Tensor for version 0.4 & higher.
    if int(pytorch_ver[0]) > 0 or int(pytorch_ver[1]) >= 4:
        output = model(img_tensor)

    # pytorch versions less than 0.4
    else:
        # apply data to model
        output = model(data)

    # return index corresponding to predicted class
    pred_idx = output.data.numpy().argmax()

    return imagenet_classes_dict[pred_idx]

def check_classifying_images(results_dic):

    if results_dic is None:
        print("\n* Doesn't Check the Results Dictionary because 'classify_images' hasn't been defined.\n")
    elif len(results_dic[next(iter(results_dic))]) < 2:
        print("\n* Doesn't Check the Results Dictionary because 'classify_images' hasn't been defined.\n")
    else:

        n_match = 0
        n_notmatch = 0
    
        # Prints all Matches first
        print("\nAll image matches:")
        print("| Name                              | Real                       | Classifier                                                        |")
        print("--------------------------------------------------------------------------------------------------------------------------------------")

        for key in results_dic:

            # Prints only if a Match Index 2 == 1
            if results_dic[key][2] == 1:

                # Increments Match counter
                n_match += 1
                print("\n{:>36}| {:>27}| {:>66}|".format(key, 
                      results_dic[key][0], results_dic[key][1]))

        print("--------------------------------------------------------------------------------------------------------------------------------------")

        # Prints all NOT-Matches next
        print("\nImages that didn't match:")
        print("| Name                              | Real                       | Classifier                                                        |")
        print("--------------------------------------------------------------------------------------------------------------------------------------")

        for key in results_dic:
        
            # Prints only if NOT-a-Match Index 2 == 0 
            if results_dic[key][2] == 0:
 
                # Increments Not-a-Match counter
                n_notmatch += 1
                print("\n{:>36}| {:>27}| {:>66}|".format(key,
                      results_dic[key][0], results_dic[key][1]))
        print("--------------------------------------------------------------------------------------------------------------------------------------")

        # Prints Total Number of Images - expects 40 from pet_images folder
        print("# Total Images",n_match + n_notmatch, "# Matches:",n_match ,
              "# NOT Matches:",n_notmatch)
        print("--------------------------------------------------------------------------------------------------------------------------------------")

 
def check_classifying_labels_as_dogs(results_dic):

    if results_dic is None:
        print("\n* Doesn't Check the Results Dictionary because 'adjust_results4_isadog' hasn't been defined.\n")
    elif len(results_dic[next(iter(results_dic))]) < 4 :
        print("\n* Doesn't Check the Results Dictionary because 'adjust_results4_isadog' hasn't been defined.\n")

    else:
        # Code for checking adjust_results4_isadog
        # Checks matches and not matches are classified correctly as "dogs" and
        # "not-dogs" Checks that all 40 images are classified as a Match or Not-a 
        # Match
    
        # Sets counters for matches & NOT-matches
        n_match = 0
        n_notmatch = 0
    
        # Prints all Matches first
        print("\n\nImages classified correctly with IS-A-DOG marks:")
        print("| Name                              | Real                       | Classifier                                                        | Image label = Dog | Classifier label = Dog |")
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

        for key in results_dic:

            # Prints only if a Match Index 2 == 1
            if results_dic[key][2] == 1:

                # Increments Match counter
                n_match += 1
                print("\n{:>36}| {:>27}| {:>66}| {:>18}| {:>23}|".format(key,
                      results_dic[key][0], results_dic[key][1], results_dic[key][3], 
                      results_dic[key][4]))

        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

        # Prints all NOT-Matches next
        print("\nINcorrect classification with IS-A-DOG marks:")
        print("| Name                              | Real                       | Classifier                                                        | Image label = Dog | Classifier label = Dog |")
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

        for key in results_dic:
        
            # Prints only if NOT-a-Match Index 2 == 0 
            if results_dic[key][2] == 0:
 
                # Increments Not-a-Match counter
                n_notmatch += 1
                print("\n{:>36}| {:>27}| {:>66}| {:>18}| {:>23}|".format(key,
                      results_dic[key][0], results_dic[key][1], results_dic[key][3], 
                      results_dic[key][4]))

        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

        # Prints Total Number of Images - expects 40 from pet_images folder
        print("# Total Images",n_match + n_notmatch, "# Matches:",n_match ,
              "# NOT Matches:",n_notmatch)
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

def check_calculating_results(results_dic, results_stats_dic):

    if results_stats_dic is None:
        print("\n* Doesn't Check the Results Dictionary because 'calculates_results_stats' hasn't been defined.\n")
    else:
        # Code for checking results_stats_dic -
        # Checks calculations of counts & percentages BY using results_dic
        # to re-calculate the values and then compare to the values
        # in results_stats_dic
    
        # Initialize counters to zero and number of images total
        n_images = len(results_dic)
        n_pet_dog = 0
        n_class_cdog = 0
        n_class_cnotd = 0
        n_match_breed = 0
    
        # Interates through results_dic dictionary to recompute the statistics
        # outside of the calculates_results_stats() function
        for key in results_dic:

            # match (if dog then breed match)
            if results_dic[key][2] == 1:

                # isa dog (pet label) & breed match
                if results_dic[key][3] == 1:
                    n_pet_dog += 1

                    # isa dog (classifier label) & breed match
                    if results_dic[key][4] == 1:
                        n_class_cdog += 1
                        n_match_breed += 1

                # NOT dog (pet_label)
                else:

                    # NOT dog (classifier label)
                    if results_dic[key][4] == 0:
                        n_class_cnotd += 1

            # NOT - match (not a breed match if a dog)
            else:
 
                # NOT - match
                # isa dog (pet label) 
                if results_dic[key][3] == 1:
                    n_pet_dog += 1

                    # isa dog (classifier label)
                    if results_dic[key][4] == 1:
                        n_class_cdog += 1

                # NOT dog (pet_label)
                else:

                    # NOT dog (classifier label)
                    if results_dic[key][4] == 0:
                        n_class_cnotd += 1

                    
        # calculates statistics based upon counters from above
        n_pet_notd = n_images - n_pet_dog
        pct_corr_dog = ( n_class_cdog / n_pet_dog )*100
        pct_corr_notdog = ( n_class_cnotd / n_pet_notd )*100
        pct_corr_breed = ( n_match_breed / n_pet_dog )*100
    
        # prints calculated statistics
        print("\n\nGeneral statistics:")
        print("\nNumber of images: {:2d}  \nNumber of images with dogs: {:2d}  \nNumber of other images: {:2d} \n\nCorrect dog classification: {:5.1f}% \nCorrect not dog classification: {:5.1f}%  \nCorrect dog's breed classification: {:5.1f}%\n".format(
              results_stats_dic['n_images'], results_stats_dic['n_dogs_img'],
              results_stats_dic['n_notdogs_img'], results_stats_dic['pct_correct_dogs'],
              results_stats_dic['pct_correct_notdogs'],
              results_stats_dic['pct_correct_breed']))
    
def adjust_results4_isadog(results_dic):
             
    dognames=set()
    
    with open("dognames.txt") as file:
        for line in file:
            dognames.add(line.lower().strip())
    
    for key, value in results_dic.items():
        if value[0] in dognames:
            value.append(1)
        else:
            value.append(0)
            
        classifier_labels=value[1].lower().strip().split(",")
        classifier_flag=0
        
        for label in classifier_labels:
            if label.strip() in dognames:
                classifier_flag=1      
        value.append(classifier_flag)
        
def calculates_results_stats(results_dic):
    
    results_stats_dic=dict()
    n_images=len(results_dic)
    n_dogs_img=0
    n_notdogs_img=0
    n_match=0
    n_correct_dogs=0
    n_correct_notdogs=0
    n_correct_breed=0
    
    for key,value in results_dic.items():
        if value[2]==1:
            n_match+=1
        
        if value[3]==1:
            n_dogs_img+=1
            if value[4]==1:
                n_correct_dogs+=1
            if value[2]==1:
                n_correct_breed+=1
        elif value[4]==0:
            n_correct_notdogs+=1
    
    n_notdogs_img=n_images-n_dogs_img
    
    results_stats_dic["n_images"]=n_images
    results_stats_dic["n_dogs_img"]=n_dogs_img
    results_stats_dic["n_notdogs_img"]=n_notdogs_img
    results_stats_dic["n_match"]=n_match
    results_stats_dic["n_correct_dogs"]=n_correct_dogs
    results_stats_dic["n_correct_notdogs"]=n_correct_notdogs
    results_stats_dic["n_correct_breed"]=n_correct_breed
    
    if n_dogs_img>0:
        results_stats_dic["pct_correct_dogs"]=n_correct_dogs/n_dogs_img*100
        results_stats_dic["pct_correct_breed"]=n_correct_breed/n_dogs_img*100
    else:
        results_stats_dic["pct_correct_dogs"]=0
        results_stats_dic["pct_correct_breed"]=0
    
    if n_notdogs_img>0:
        results_stats_dic["pct_correct_notdogs"]=n_correct_notdogs/n_notdogs_img*100
    else:
        results_stats_dic["pct_correct_notdogs"]=0
        
    if n_images>0:
        results_stats_dic["pct_match"]=n_match/n_images*100
    else:
        results_stats_dic["pct_match"]=0
        
    return results_stats_dic

def print_results(results_dic, results_stats_dic, model, 
                  print_incorrect_dogs = False, print_incorrect_breed = False):

    print("\nClassification results:")

    for key, value in results_stats_dic.items():
        print("{}: {}".format(key, value))     


# Main program function defined below
def main():
   
    start_time = time()
    
    # Define get_input_args function within the file get_input_args.py
    # This function retrieves 3 Command Line Arugments from user as input from
    # the user running the program from a terminal window. This function returns
    # the collection of these command line arguments from the function call as
    # the variable in_arg
    in_arg = get_input_args()

    # Function that checks command line arguments using in_arg 
    # Uncommemt line 29 to print full details 
    check_command_line_arguments(in_arg)

    # Define get_pet_labels function within the file get_pet_labels.py
    # Once the get_pet_labels function has been defined replace 'None' 
    # in the function call with in_arg.dir  Once you have done the replacements
    # your function call should look like this: 
    #             get_pet_labels(in_arg.dir)
    # This function creates the results dictionary that contains the results, 
    # this dictionary is returned from the function call as the variable results
    
    results = get_pet_labels(in_arg.dir)

    # Function that checks Pet Images in the results Dictionary using results     
    #check_creating_pet_image_labels(results)


    # Classify_images function within the file classiy_images.py
    # Once the classify_images function has been defined replace first 'None' 
    # in the function call with in_arg.dir and replace the last 'None' in the
    # function call with in_arg.arch  Once you have done the replacements your
    # function call should look like this: 
    #             classify_images(in_arg.dir, results, in_arg.arch)
    # Creates Classifier Labels with classifier function, Compares Labels, 
    # and adds these results to the results dictionary - results
    classify_images(in_arg.dir, results)

    # Function that checks Results Dictionary using results     
    #check_classifying_images(results)    

    # Adjust_results4_isadog function within the file adjust_results4_isadog.py
    # Once the adjust_results4_isadog function has been defined replace 'None' 
    # in the function call with in_arg.dogfile  Once you have done the 
    # replacements your function call should look like this: 
    #          adjust_results4_isadog(results, in_arg.dogfile)
    # Adjusts the results dictionary to determine if classifier correctly 
    # classified images as 'a dog' or 'not a dog'. This demonstrates if 
    # model can correctly classify dog images as dogs (regardless of breed)
    adjust_results4_isadog(results)

    # Function that checks Results Dictionary for is-a-dog adjustment using results
    #check_classifying_labels_as_dogs(results)

    # Calculates_results_stats function within the file calculates_results_stats.py
    # This function creates the results statistics dictionary that contains a
    # summary of the results statistics (this includes counts & percentages). This
    # dictionary is returned from the function call as the variable results_stats    
    # Calculates results of run and puts statistics in the Results Statistics
    # Dictionary - called results_stats
    results_stats = calculates_results_stats(results)

    # Function that checks Results Statistics Dictionary using results_stats

    check_calculating_results(results, results_stats)


    # Print_results function within the file print_results.py
    # Prints summary results, incorrect classifications of dogs (if requested)
    # and incorrectly classified breeds (if requested)
    #print_results(results, results_stats, "vgg", True, True)
    
    # Measure total program runtime by collecting end time & prints it in hh:mm:ss format
    end_time = time()
     
    tot_time = end_time-start_time
    print("\nTotal Elapsed Runtime:",
          str(round((tot_time/3600)))+":"+str(round((tot_time%3600)/60))+":"
          +str(round((tot_time%3600)%60)) )
    
if __name__ == "__main__":
    main()

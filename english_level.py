import os
import textstat
import nltk
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
import numpy as np

nltk.download('punkt')  # Download the Punkt tokenizer

# Define the series list
series_list = ["StarTrek", "NextGen", "DS9", "Voyager", "Enterprise", "STDisco17", "StarTrekPIC"]

# Function to convert English word to number
def word_to_number(word):
    word_number_dict = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7, "Eight": 8, "Nine": 9, "Ten": 10}
    return word_number_dict.get(word, 0)

# Initialize a dictionary to store the grade levels
complexity_scores = {}

# Iterate over each series
for series in series_list:
    print(f"\nProcessing {series}...")

    # Iterate over each season in the series directory
    for season in os.listdir(series):
        if season.startswith("Season"):
        
            season_number = season.split(" ")[1]
        
            # Initialize the dictionaries for other readability and complexity scores for this season
            complexity_scores[f"{series}_Season_{season_number}"] = {
                "flesch_kincaid": [],
                "dale_chall": [],
                "gunning_fog": [],
                "smog": [],
                "coleman_liau": [],
                "lexical_diversity": [],
                "average_word_length": [],
                "vocabulary_richness": []
            }

            # Iterate over each episode in the season directory
            for episode in os.listdir(f"{series}/{season}"):
                # Read the transcript file
                with open(f"{series}/{season}/{episode}", 'r') as f:
                    transcript_text = f.read()

                # Tokenize the transcript text
                words = word_tokenize(transcript_text)

                # Compute the readability and complexity scores of the transcript
                flesch_kincaid = textstat.flesch_kincaid_grade(transcript_text)
                dale_chall = textstat.dale_chall_readability_score(transcript_text)
                gunning_fog = textstat.gunning_fog(transcript_text)
                smog = textstat.smog_index(transcript_text)
                coleman_liau = textstat.coleman_liau_index(transcript_text)
                lexical_diversity = len(set(words)) / len(words)
                average_word_length = sum(len(word) for word in words) / len(words)
                vocabulary_richness = len(set(words)) / np.sqrt(2*len(words))

                # Store the readability and complexity scores
                complexity_scores[f"{series}_Season_{season_number}"]["flesch_kincaid"].append(flesch_kincaid)
                complexity_scores[f"{series}_Season_{season_number}"]["dale_chall"].append(dale_chall)
                complexity_scores[f"{series}_Season_{season_number}"]["gunning_fog"].append(gunning_fog)
                complexity_scores[f"{series}_Season_{season_number}"]["smog"].append(smog)
                complexity_scores[f"{series}_Season_{season_number}"]["coleman_liau"].append(coleman_liau)
                complexity_scores[f"{series}_Season_{season_number}"]["lexical_diversity"].append(lexical_diversity)
                complexity_scores[f"{series}_Season_{season_number}"]["average_word_length"].append(average_word_length)
                complexity_scores[f"{series}_Season_{season_number}"]["vocabulary_richness"].append(vocabulary_richness)

    print(f"\nFinished processing {series}.")

# Plotting
for complexity_measure in ["flesch_kincaid", "dale_chall", "gunning_fog", "smog", "coleman_liau", "lexical_diversity", "average_word_length", "vocabulary_richness"]:
    fig, ax = plt.subplots()

    # Compute average scores for each season
    labels = sorted(complexity_scores.keys(), key=lambda x: (series_list.index(x.split('_')[0]), word_to_number(x.split('_')[2])))
    scores = [np.mean(complexity_scores[season][complexity_measure]) for season in labels]

    ax.bar(labels, scores)
    ax.set_title(f'Average {complexity_measure.replace("_", " ").title()} Scores')
    ax.set_xlabel('Series and Season')
    ax.set_ylabel('Score')
    plt.xticks(rotation=90)  # Rotate x-axis labels for better readability

    # Compute the average complexity score for each series and add a dotted line for each of them in the plot.
    for series in series_list:
        indices = [i for i, label in enumerate(labels) if label.startswith(series+"_")]
        if indices:
            mean_score = np.mean([scores[i] for i in indices])
            ax.plot([indices[0], indices[-1]], [mean_score, mean_score], color='black')

    ax.set_xlim(left=-0.5, right=len(labels)-0.5)  # Set the x-axis limits to fit the bars exactly

    plt.tight_layout()
    plt.savefig(f"{complexity_measure}_scores.png", dpi=300)
    plt.close()  # Close the plot

    print(f"\nSaved plot for {complexity_measure}.")

#
#import os
#import textstat
#import matplotlib.pyplot as plt
#import numpy as np
#
## Define the series list
#series_list = ["StarTrek", "NextGen", "DS9", "Voyager", "Enterprise", "STDisco17", "StarTrekPIC"]
#
## Function to convert English word to number
#def word_to_number(word):
#    word_number_dict = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7, "Eight": 8, "Nine": 9, "Ten": 10}
#    return word_number_dict.get(word, 0)
#
## Initialize a dictionary to store the grade levels
#readability_scores = {}
#
## Iterate over each series
#for series in series_list:
#    print(f"\nProcessing {series}...")
#
#    # Iterate over each season in the series directory
#    for season in os.listdir(series):
#        if season.startswith("Season"):
#        
#            season_number = season.split(" ")[1]
#        
#            # Initialize the dictionaries for other readability scores for this season
#            readability_scores[f"{series}_Season_{season_number}"] = {
#                "flesch_kincaid": [],
#                "dale_chall": [],
#                "gunning_fog": [],
#                "smog": [],
#                "coleman_liau": []
#            }
#
#            # Iterate over each episode in the season directory
#            for episode in os.listdir(f"{series}/{season}"):
#                # Read the transcript file
#                with open(f"{series}/{season}/{episode}", 'r') as f:
#                    transcript_text = f.read()
#
#                # Compute the readability scores of the transcript
#                flesch_kincaid = textstat.flesch_kincaid_grade(transcript_text)
#                dale_chall = textstat.dale_chall_readability_score(transcript_text)
#                gunning_fog = textstat.gunning_fog(transcript_text)
#                smog = textstat.smog_index(transcript_text)
#                coleman_liau = textstat.coleman_liau_index(transcript_text)
#
#                # Store the readability scores
#                readability_scores[f"{series}_Season_{season_number}"]["flesch_kincaid"].append(flesch_kincaid)
#                readability_scores[f"{series}_Season_{season_number}"]["dale_chall"].append(dale_chall)
#                readability_scores[f"{series}_Season_{season_number}"]["gunning_fog"].append(gunning_fog)
#                readability_scores[f"{series}_Season_{season_number}"]["smog"].append(smog)
#                readability_scores[f"{series}_Season_{season_number}"]["coleman_liau"].append(coleman_liau)
#
#    print(f"\nFinished processing {series}.")
#
## Plotting
#for readability_measure in ["flesch_kincaid", "dale_chall", "gunning_fog", "smog", "coleman_liau"]:
#    fig, ax = plt.subplots()
#
#    # Compute average scores for each season
#    labels = sorted(readability_scores.keys(), key=lambda x: (series_list.index(x.split('_')[0]), word_to_number(x.split('_')[2])))
#    scores = [np.mean(readability_scores[season][readability_measure]) for season in labels]
#
#    ax.bar(labels, scores)
#    ax.set_title(f'Average {readability_measure.replace("_", " ").title()} Scores')
#    ax.set_xlabel('Series and Season')
#    ax.set_ylabel('Score')
#    plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
#
#    # Compute the average readability score for each series and add a dotted line for each of them in the plot.
#    for series in series_list:
#        indices = [i for i, label in enumerate(labels) if label.startswith(series+"_")]
#        if indices:
#            mean_score = np.mean([scores[i] for i in indices])
#            print(indices[0])
#            print(indices[-1])            
#            ax.plot([indices[0], indices[-1]], [mean_score, mean_score], color='black')
#
#    ax.set_xlim(left=-0.5, right=len(labels)-0.5)  # Set the x-axis limits to fit the bars exactly
#
#    plt.tight_layout()
#    plt.savefig(f"{readability_measure}_scores.png", dpi=300)
#    plt.close()  # Close the plot
#
#    print(f"\nSaved plot for {readability_measure}.")
#
##
##import os
##import textstat
##import matplotlib.pyplot as plt
##import numpy as np
##
##def word_to_number(word):
##    word_number_dict = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7, "Eight": 8, "Nine": 9, "Ten": 10}
##    return word_number_dict.get(word, 0)
##                                
### Define the series list
##series_list = ["StarTrek", "NextGen", "DS9", "Voyager", "Enterprise", "STDisco17", "StarTrekPIC"]
##
### Initialize a dictionary to store the grade levels
##readability_scores = {}
##
### Iterate over each series
##for series in series_list:
##    print(f"\nProcessing {series}...")
##
##    # Iterate over each season in the series directory
##    for season in os.listdir(series):
##        if season.startswith("Season"):
##        
##            season_number = season.split(" ")[1]
##        
##            # Initialize the dictionaries for other readability scores for this season
##            readability_scores[f"{series}_Season_{season_number}"] = {
##                "flesch_kincaid": [],
##                "dale_chall": [],
##                "gunning_fog": [],
##                "smog": [],
##                "coleman_liau": []
##            }
##
##            # Iterate over each episode in the season directory
##            for episode in os.listdir(f"{series}/{season}"):
##                # Read the transcript file
##                with open(f"{series}/{season}/{episode}", 'r') as f:
##                    transcript_text = f.read()
##
##                # Compute the Flesch-Kincaid grade level of the transcript
##                flesch_kincaid = textstat.flesch_kincaid_grade(transcript_text)
##
##                # Compute the other readability scores of the transcript
##                dale_chall = textstat.dale_chall_readability_score(transcript_text)
##                gunning_fog = textstat.gunning_fog(transcript_text)
##                smog = textstat.smog_index(transcript_text)
##                coleman_liau = textstat.coleman_liau_index(transcript_text)
##
##                # Store the readability scores
##                readability_scores[f"{series}_Season_{season_number}"]["flesch_kincaid"].append(flesch_kincaid)
##                readability_scores[f"{series}_Season_{season_number}"]["dale_chall"].append(dale_chall)
##                readability_scores[f"{series}_Season_{season_number}"]["gunning_fog"].append(gunning_fog)
##                readability_scores[f"{series}_Season_{season_number}"]["smog"].append(smog)
##                readability_scores[f"{series}_Season_{season_number}"]["coleman_liau"].append(coleman_liau)
##
##    print(f"\nFinished processing {series}.")
##
##
##import os
##import textstat
##import matplotlib.pyplot as plt
##import numpy as np
##
### Define the series list
##series_list = ["StarTrek", "NextGen", "DS9", "Voyager", "Enterprise", "STDisco17", "StarTrekPIC"]
##
### Function to convert English word to number
##def word_to_number(word):
##    word_number_dict = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7, "Eight": 8, "Nine": 9, "Ten": 10}
##    return word_number_dict.get(word, 0)
##
### Initialize a dictionary to store the grade levels
##readability_scores = {}
##
### Iterate over each series
##for series in series_list:
##    print(f"\nProcessing {series}...")
##
##    # Iterate over each season in the series directory
##    for season in os.listdir(series):
##        if season.startswith("Season"):
##        
##            season_number = season.split(" ")[1]
##        
##            # Initialize the dictionaries for other readability scores for this season
##            readability_scores[f"{series}_Season_{season_number}"] = {
##                "flesch_kincaid": [],
##                "dale_chall": [],
##                "gunning_fog": [],
##                "smog": [],
##                "coleman_liau": []
##            }
##
##            # Iterate over each episode in the season directory
##            for episode in os.listdir(f"{series}/{season}"):
##                # Read the transcript file
##                with open(f"{series}/{season}/{episode}", 'r') as f:
##                    transcript_text = f.read()
##
##                # Compute the readability scores of the transcript
##                flesch_kincaid = textstat.flesch_kincaid_grade(transcript_text)
##                dale_chall = textstat.dale_chall_readability_score(transcript_text)
##                gunning_fog = textstat.gunning_fog(transcript_text)
##                smog = textstat.smog_index(transcript_text)
##                coleman_liau = textstat.coleman_liau_index(transcript_text)
##
##                # Store the readability scores
##                readability_scores[f"{series}_Season_{season_number}"]["flesch_kincaid"].append(flesch_kincaid)
##                readability_scores[f"{series}_Season_{season_number}"]["dale_chall"].append(dale_chall)
##                readability_scores[f"{series}_Season_{season_number}"]["gunning_fog"].append(gunning_fog)
##                readability_scores[f"{series}_Season_{season_number}"]["smog"].append(smog)
##                readability_scores[f"{series}_Season_{season_number}"]["coleman_liau"].append(coleman_liau)
##
##    print(f"\nFinished processing {series}.")
##
### Plotting
##for readability_measure in ["flesch_kincaid", "dale_chall", "gunning_fog", "smog", "coleman_liau"]:
##    fig, ax = plt.subplots()
##
##    # Compute average scores for each season
##    labels = sorted(readability_scores.keys(), key=lambda x: (series_list.index(x.split('_')[0]), word_to_number(x.split('_')[2])))
##    scores = [np.mean(readability_scores[season][readability_measure]) for season in labels]
##
##    ax.bar(labels, scores)
##    ax.set_title(f'Average {readability_measure.replace("_", " ").title()} Scores')
##    ax.set_xlabel('Series and Season')
##    ax.set_ylabel('Score')
##    plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
##
##    # Compute the average readability score for each series and add a dotted line for each of them in the plot.
##    for series in series_list:
##        indices = [i for i, label in enumerate(labels) if label.startswith(series)]
##        if indices:
##            mean_score = np.mean([scores[i] for i in indices])
##            ax.plot([indices[0], indices[-1]], [mean_score, mean_score], color='black')
##
##    plt.tight_layout()
##    plt.savefig(f"{readability_measure}_scores.png", dpi=300)
##    plt.close()  # Close the plot
##
##    print(f"\nSaved plot for {readability_measure}.")
##
##    
#### Plotting
###for readability_measure in ["flesch_kincaid", "dale_chall", "gunning_fog", "smog", "coleman_liau"]:
###    fig, ax = plt.subplots()
###
###    # Compute average scores for each season
###    labels = sorted(readability_scores.keys(), key=lambda x: (series_list.index(x.split('_')[0]), word_to_number(x.split('_')[2])))
###    scores = [np.mean(readability_scores[season][readability_measure]) for season in labels]
###
###    ax.bar(labels, scores)
###    ax.set_title(f'Average {readability_measure.replace("_", " ").title()} Scores')
###    ax.set_xlabel('Series and Season')
###    ax.set_ylabel('Score')
###    plt.xticks(rotation=90)
###
###    # Add average line per series
###    for series in series_list:
###        indices = [i for i, label in enumerate(labels) if label.startswith(series)]
###        if indices:
###            mean_score = np.mean([scores[i] for i in indices])
###            ax.plot([indices[0], indices[-1]], [mean_score, mean_score], color='black')
###
###    plt.show()
###
####    
##### Plotting
####for readability_measure in ["flesch_kincaid", "dale_chall", "gunning_fog", "smog", "coleman_liau"]:
####    fig, ax = plt.subplots()
####
####    # Compute average scores for each season
####
####    # Then in your sorting function:
####    labels = sorted(readability_scores.keys(), key=lambda x: (x.split('_')[0], word_to_number(x.split('_')[2])))
####    scores = [np.mean(readability_scores[season][readability_measure]) for season in labels]
####
####    ax.bar(labels, scores)
####    ax.set_title(f'Average {readability_measure.replace("_", " ").title()} Scores')
####    ax.set_xlabel('Series and Season')
####    ax.set_ylabel('Score')
####    plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
####
####    # Compute the average readability score for each series and add a dotted line for each of them in the plot.
####    series_averages = {}
####
####    for series in series_list:
####        series_seasons = [season for season in labels if season.split('_')[0] == series]
####        series_scores = [readability_scores[season][readability_measure] for season in series_seasons]
####        series_averages[series] = np.mean([score for season_scores in series_scores for score in season_scores])
####
####    # Color dictionary for each series
####    color_dict = {
####        "StarTrek": "blue",
####        "NextGen": "green",
####        "DS9": "red",
####        "Voyager": "purple",
####        "Enterprise": "brown",
####        "STDisco17": "pink",
####        "StarTrekPIC": "orange"
####    }
####
####    for series, average in series_averages.items():
####        ax.axhline(y=average, color=color_dict[series], linestyle='dotted')
####
####        # Adding average score annotation for each series
####        series_last_season = sorted([season for season in labels if season.split('_')[0] == series])[-1]
####        plt.text(series_last_season, average, f'Avg: {average:.2f}', color=color_dict[series], ha='right', va='center')
####
####    plt.tight_layout()
####    plt.savefig(f"{readability_measure}_scores.png", dpi=300)
####    plt.close()  # Close the plot
####
####    print(f"\nSaved plot for {readability_measure}.")
####
###
##
#

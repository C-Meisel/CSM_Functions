''' This module contains functions to help format and plot XRD files
# C-Meisel
'''

'Imports'
import pandas as pd
import matplotlib.pyplot as plt
import csv

def xrd_format(location): #Used on a CSV from the XRD machine to format the data for plotting and convert intensity to relative intensity.  The input is a string
    file = csv.reader(open(location, "r",encoding='latin1')) #I honestly dk what is going on here
    for row in file: #searches first column of each row in csv for "Angle", then subtracts 1. This gives the right amount of rows to skip to get to the XRD data
        if row[0] == 'Angle':
            skip = file.line_num-1
            break
    df = pd.read_csv(location,skiprows=skip) #creates datafile from csv convert of XRDML file
    maximum = df['Intensity'].max() #calculates highes intensity value
    df['Intensity'] = df['Intensity']/maximum #
    df = df.rename({'Angle':'a','Intensity':'i'},axis=1) #renames columns to make further plotting quicker a = angle i = relative intensity
    return df

def xrd_format_icdd(sheet): #Returns 2Theta and relative intensity data from my saved ICDD files. The input is the name of the sheet (material name)
    df = pd.read_excel('/Users/Charlie/Documents/CSM/XRD_Data/ICDD_XRD_Files.xlsx',sheet) #will need to change this line if the file location changes
    df = df[['2Theta','Relative Intensity']]
    df = df.rename({'2Theta':'a','Relative Intensity':'i'},axis=1)
    return df

def plot_xrd(loc,material): #this function graphs the XRD spectra from a CSV. Both inputs are strings. Loc is the location of the file. material is what the line will be named
    df = xrd_format(loc)
    # plt.figure(dpi=250)  #change to change the quality of the return chart
    plt.plot(df['a'],df['i'], label = material)
    plt.xlim(20,80)
    plt.xlabel('2\u03B8')
    plt.ylabel('Relative Intensity')
    plt.tight_layout()
    plt.legend()

def plot_xrds(loc, material,y_offset=0,linewidth=1.5): #This function enables multiple spectra to be on the same plot. this function graphs the XRD spectra from a CSV. loc and material inputs are strings, while y_offset is the y offset and if left blank defaults to 0. Loc is the location of the file. material is what the line will be named
    try: #loc should be the sheet name in the ICDD file or the location of the csv file
        df = xrd_format_icdd(loc) 
    except:
        df = xrd_format(loc)
    plt.plot(df['a'],df['i']+y_offset, label = material,linewidth=linewidth) #offset is the y axis offset to stack graphs and is optional
    plt.xlabel('2\u03B8',size='x-large')
    plt.ylabel('Relative Intensity',size='x-large')
    plt.xticks(fontsize = 'large')
    plt.yticks(fontsize = 'large')
    plt.tight_layout()
    plt.legend(fontsize='large')
import pandas
from bokeh.layouts import layout
from bokeh.models.glyphs import Circle
from bokeh.models.sources import ColumnDataSource
from bokeh.plotting import figure
from bokeh.io import curdoc, show
from numpy import source
import pandas
from bokeh.sampledata.iris import flowers
from bokeh.models import Range1d, PanTool, ResetTool, HoverTool, Band, Toggle
from bokeh.models.annotations import Label, LabelSet, Span, BoxAnnotation
from bokeh.models.widgets import Select, Slider, RadioButtonGroup
from bokeh.layouts import gridplot

data = pandas.read_csv("/Users/tansubaktiran1/Dropbox/LEARNING/PYTHON/HOBBY/GURUR_TEST/DATA.csv", sep=",")

data = data.dropna()

data["PREM_DIFF"] = data["SALES REV PREMIUM"]-data["SALES BUDG PREMIUM"]
#data["SALES PROFIT PREMIUM"] = data["SALES PROFIT PREMIUM"].str.replace(",",".").astype(float)
#data["SALES PROFIT ECO"] = data["SALES PROFIT ECO"].str.replace(",",".").astype(float)

Max_val_x = data["SALES REV PREMIUM"].max()
Max_val_x = Max_val_x*1.1
#Max_val_x = Max_val_x.round(decimals=0)
Max_val_x2 = data["SALES REV ECO"].max()
Max_val_x2 = Max_val_x2*1.1
#Max_val_x2 = Max_val_x2.round(decimals=0)

Ave_prof_Prem = data["SALES PROFIT PREMIUM"].mean()
Ave_prof_Prem_hi_band = Ave_prof_Prem*1.2
Ave_prof_Prem_lo_band = Ave_prof_Prem/1.2

Ave_prof_Eco = data["SALES PROFIT ECO"].mean()
Ave_prof_Eco_hi_band = Ave_prof_Eco*1.2
Ave_prof_Eco_lo_band = Ave_prof_Eco/1.2

#For F3 calculations
dealers = data[["REGION", "NUMBER OF DEALERS", "NUMBER OF NEW DEALERS", "NUMBER OF ON-BUDGET DEALERS", "NUMBER OF PERFORMANCE DEALERS"]].copy()
dealers["NUMBER OF NEW DEALERS_magn"] = dealers["NUMBER OF NEW DEALERS"]*10
dealers["NUMBER OF PERFORMANCE DEALERS_magn"] = dealers["NUMBER OF PERFORMANCE DEALERS"]*10
dealers["NUMBER OF DEALERS_magn"] = dealers["NUMBER OF DEALERS"]*2
dealers["NUMBER OF ON-BUDGET DEALERS_magn"] = dealers["NUMBER OF ON-BUDGET DEALERS"]*2

dealers["NEW_TO_TOT_DEALER"] = dealers["NUMBER OF NEW DEALERS"]/dealers["NUMBER OF DEALERS"]
dealers["ONBD_TO_TOT_DEALER"] = dealers["NUMBER OF ON-BUDGET DEALERS"]/dealers["NUMBER OF DEALERS"]
dealers["PERF_TO_TOT_DEALER"] = dealers["NUMBER OF PERFORMANCE DEALERS"]/dealers["NUMBER OF DEALERS"]

#-------- burasını geliştirebiliriz..
dealers["PERF_TO_TOT_DEALER"] = dealers["PERF_TO_TOT_DEALER"]*100
dealers["PERF_TO_TOT_DEALER"] = (dealers["PERF_TO_TOT_DEALER"]).round(decimals=0)
dealers["test_df"] = "%"
dealers["PERF_TO_TOT_DEALER"] = dealers["PERF_TO_TOT_DEALER"].astype(int)
dealers["PERF_TO_TOT_DEALER"] = dealers["PERF_TO_TOT_DEALER"].astype(str)

dealers["PERF_TO_TOT_DEALER_perc"] = dealers["PERF_TO_TOT_DEALER"] + dealers["test_df"]

dealers["ONBD_TO_TOT_DEALER"] = dealers["ONBD_TO_TOT_DEALER"]*100
dealers["ONBD_TO_TOT_DEALER"] = dealers["ONBD_TO_TOT_DEALER"].astype(int)
dealers["ONBD_TO_TOT_DEALER"] = dealers["ONBD_TO_TOT_DEALER"].astype(str)

dealers["ONBD_TO_TOT_DEALER_perc"] = dealers["ONBD_TO_TOT_DEALER"] + dealers["test_df"]


dealers["NEW_TO_TOT_DEALER"] = dealers["NEW_TO_TOT_DEALER"]*100
dealers["NEW_TO_TOT_DEALER"] = dealers["NEW_TO_TOT_DEALER"].astype(int)
dealers["NEW_TO_TOT_DEALER"] = dealers["NEW_TO_TOT_DEALER"].astype(str)

dealers["NEW_TO_TOT_DEALER_perc"] = dealers["NEW_TO_TOT_DEALER"] + dealers["test_df"] 

print(dealers["PERF_TO_TOT_DEALER_perc"])

def find_max_performer(df):
    max_val = df.max()
    max_val_index=df.idxmax(axis=0)
    data.iloc[:,0]
    #print(max_val_index)
    #print(data.iloc[max_val_index,0])
    return max_val_index

max_sales_rev_pre_ind = find_max_performer(data["SALES VOLUME PREMIUM"])
max_sales_rev_eco_ind = find_max_performer(data["SALES VOLUME ECO"])
max_sales_rev_prev_period = find_max_performer(data["PREVIOUS CYCLE TOTAL SALES REVENUES"])



#Best Performer____________TTTTTTTTTTTTTTTTT
source = ColumnDataSource(data)
source2 = ColumnDataSource(dealers) #For F3

#F3 Region____________
f3 = figure(x_range=dealers["REGION"])
f3.circle(x="REGION" , y=1.0, size="NUMBER OF DEALERS_magn", color="orangered", 
fill_alpha=.7,  source=source2, legend_label="Number of Dealers")
f3.circle(x="REGION" , y=2.5, size="NUMBER OF ON-BUDGET DEALERS_magn", color="yellowgreen", 
fill_alpha=.7,  source=source2, legend_label="Number of On-Budget Dealers")
f3.circle(x="REGION" , y=.25, size=30, color="mediumblue", 
fill_alpha=.4,  source=source2, legend_label="Number of New Dealers")

f3.legend.background_fill_alpha = 0.1
f3.legend.margin = 2
f3.legend.padding = 0
f3.legend.click_policy="hide"
f3.legend.location = 'bottom_right'
f3.legend.spacing = 2
f3.legend.orientation = "horizontal"

f3.y_range = Range1d(start=-3, end=5)
f3.yaxis.visible = False
f3.plot_width = 1000
f3.plot_height = 250

dealer_labels1 = LabelSet(x="REGION", y=1, text="NUMBER OF DEALERS", x_offset=0, y_offset=0, 
text_align="center", text_baseline="middle",text_font_size="11px", text_color="white", source=source2)
f3.add_layout(dealer_labels1)
dealer_labels2 = LabelSet(x="REGION", y=2.5, text="NUMBER OF ON-BUDGET DEALERS", x_offset=0, y_offset=0, 
text_align="center", text_baseline="middle",text_font_size="11px", text_color="white", source=source2)
f3.add_layout(dealer_labels2)

dealer_labels2b = LabelSet(x="REGION", y=0.25, text="NUMBER OF NEW DEALERS", x_offset=0, y_offset=0, 
text_align="center", text_baseline="middle",text_font_size="11px", text_color="white", source=source2)
f3.add_layout(dealer_labels2b)

"""dealer_labels3 = LabelSet(x="REGION", y=3, text="ONBD_TO_TOT_DEALER_perc", x_offset=0, y_offset=0, 
text_align="center", text_baseline="middle",text_font_size="12px", text_color="red", 
background_fill_color='white', background_fill_alpha=0.8, source=source2)
f3.add_layout(dealer_labels3)"""


#Best Performer____________TTTTTTTTTTTTTTTTT
explanation1 = "Pre. Pr. Best Rev Performer"
description=Label(x=max_sales_rev_pre_ind, y=3.5, text=explanation1 ,render_mode="css", text_font_size="6pt", 
text_color='orangered', text_alpha=1, text_baseline='bottom', text_align='left',
background_fill_color='gray', background_fill_alpha=0.2, text_line_height=40)
f3.add_layout(description)

explanation2 = "Eco. Pr. Best Rev Performer"
description2=Label(x=max_sales_rev_eco_ind, y=4, text=explanation2 ,render_mode="css", text_font_size="6pt", 
text_color='orangered', text_alpha=1, text_baseline='bottom', text_align='left',
background_fill_color='gray', background_fill_alpha=0.2, text_line_height=40)
f3.add_layout(description2)
print(max_sales_rev_eco_ind)

explanation3 = "Previous Cycle Best Rev Performer"
description3=Label(x=max_sales_rev_prev_period, y=4, text=explanation3 ,render_mode="css", text_font_size="6pt", 
text_color='orangered', text_alpha=1, text_baseline='bottom', text_align='left',
background_fill_color='gray', background_fill_alpha=0.2, text_line_height=40)
f3.add_layout(description3)


#F4 Region____________
f4 = figure(x_range=dealers["REGION"])
f4.circle(x="REGION" , y=.5, size="NUMBER OF NEW DEALERS_magn", color="mediumblue", 
fill_alpha=.6,  source=source2, legend_label="Number of New Dealers")
f4.circle(x="REGION" , y=1, size="NUMBER OF PERFORMANCE DEALERS_magn", color="darkturquoise", 
fill_alpha=.6,  source=source2, legend_label="Number of Performance Dealers")

f4.legend.background_fill_alpha = 0.1
f4.legend.margin = 2
f4.legend.padding = 2
f4.legend.click_policy="hide"
f4.legend.location = 'bottom_right'

f4.y_range = Range1d(start=-1, end=1.75)
f4.yaxis.visible = False
f4.plot_width = 1000
f4.plot_height = 250

dealer_labels4 = LabelSet(x="REGION", y=.5, text="NUMBER OF NEW DEALERS", x_offset=0, y_offset=0, 
text_align="center", text_baseline="middle",text_font_size="11px", text_color="white", source=source2)
f4.add_layout(dealer_labels4)
dealer_labels5 = LabelSet(x="REGION", y=1, text="NUMBER OF PERFORMANCE DEALERS", x_offset=0, y_offset=0, 
text_align="center", text_baseline="middle",text_font_size="11px", text_color="white", source=source2)
f4.add_layout(dealer_labels5)

dealer_labels6 = LabelSet(x="REGION", y=0, text="NEW_TO_TOT_DEALER_perc", x_offset=0, y_offset=0, 
text_align="center", text_baseline="middle",text_font_size="10px", text_color="red", text_alpha=0,
background_fill_color='white', background_fill_alpha=0, source=source2)
f4.add_layout(dealer_labels6)

dealer_labels7=LabelSet(x="REGION", y=1.6, text="PERF_TO_TOT_DEALER_perc", x_offset=0, y_offset=0, render_mode="css", 
text_font_size="10px", text_color='red', text_alpha=0, text_baseline='bottom', text_align='center',
background_fill_color='white', background_fill_alpha=0, source=source2)
f4.add_layout(dealer_labels7)
#------------burada

dealer_labels3 = LabelSet(x="REGION", y=3.2, text="ONBD_TO_TOT_DEALER_perc", x_offset=0, y_offset=0, 
text_align="center", text_baseline="middle",text_font_size="10px", text_color="black", text_alpha=0,
background_fill_color='turquoise', background_fill_alpha=0, source=source2)
f3.add_layout(dealer_labels3)

#------------burada


show_average_decision = 0
def show_percentages(arg):
    global show_average_decision
    show_average_decision = show_average_decision +1
    dealer_labels6.text_alpha = (show_average_decision%2)
    dealer_labels6.background_fill_alpha = (show_average_decision%2)
    dealer_labels3.text_alpha = (show_average_decision%2)
    dealer_labels3.background_fill_alpha = (show_average_decision%2)
    dealer_labels7.text_alpha = (show_average_decision%2)
    dealer_labels7.background_fill_alpha = (show_average_decision%2)

dealer_labels3
toggle1 = Toggle(label="Show percentages (ratio to total nr. of dealers)", button_type="success", active=True)
toggle1.on_click(show_percentages)

#------------burada
#dealer_layout = gridplot([[f3],[f4]])
#-----------------------------------------------------------


lay_out2 = layout([[toggle1]])
dealer_layout = gridplot([[f3],[f4]],plot_width=1000, plot_height=220)

curdoc().add_root(dealer_layout)
curdoc().add_root(lay_out2)


#show(dealer_layout)
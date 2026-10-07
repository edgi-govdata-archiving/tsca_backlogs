import plotly.express as px
import pandas as pd
import plotly.io as pio
import matplotlib.pyplot as plt
pio.renderers.default = "browser"


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 150)

# import data
nocs = pd.read_csv("./chemview_reports/nocs_20260925_csv.csv")
pmns = pd.read_csv("./chemview_reports/pmn_snun_mcans_20260925_csv.csv")
subs = pd.read_csv("./chemview_reports/submissions_20260925_csv.csv")
test = pd.read_csv("./chemview_reports/test_info_20260925_csv.csv")
nots = pd.read_csv("./web_data/chem_det_not_likely_20260925_csv.csv")
pmns2 = pd.read_csv("./web_data/pmns_snuns_20260925_csv.csv")

#---printing raw datasets--

print("Notices of Commencement (ChemView)")
for col in nocs.columns:
    print(col)
print(nocs.head(10))

print("'If Amendment, Type of Amendment' Categories:'")
categories = nocs['If Amendment, Type Of Amendment'].unique()
print(sorted(categories))

print("-----------------------")

print("Test Info (ChemView)")
for col in test.columns:
    print(col)
print(test.head(10))
print("-----------------------")

print("PMNs, SNUNs, MCANs (ChemView)")
for col in pmns.columns:
    print(col)
print(pmns.head(10))
print("-----------------------")

print("Submissions (ChemView)")
subs.sort_values(by=["Case Number"])
for col in subs.columns:
    print(col)
print(subs.head(10))

print("'Source Name' Categories:'")
categories = subs['Source Name'].unique()
print(sorted(categories))
print("-----------------------")

print("'Not Likely' Determinations")
for col in nots.columns:
    print(col)
print(nots.head(10))
print("-----------------------")


print("PMNs & SNUNs")
for col in pmns2.columns:
    print(col)
print(pmns2.head(10))
print("-----------------------")

#---data exploration--

#checking for sub duplicates 
subs = subs.sort_values(by=["EPA Received Date"], ascending=[False])
print("subs original length:", len(subs.index))
#subs = subs.drop_duplicates(subset=["Case Number", "EPA Received Date"], keep='first')
#subs = subs.drop_duplicates(subset=["Case Number", "Source Name"], keep='first')
#print("subs no duplicates length:", len(subs.index))

subs["EPA Received Date"] = pd.to_datetime(subs["EPA Received Date"])
subs["Version Published Date"] = pd.to_datetime(subs["Version Published Date"])

#graph subs categories
subs['Source Name'].value_counts().plot(kind='bar')

#plotting subs timeline
#currently opens browser for interactivity (IDE option available)
test_subs = subs.head(400)
fig = px.timeline(test_subs, x_start="EPA Received Date", x_end="Version Published Date", y="Case Number", color="Source Name")
fig.show()



#---misc exploration--
# subs_commence = subs[subs["Source Name"] == "Notice of Commencement"]
# print(subs_commence.head(10))

# nocs.sort_values(by=["Case Number"])
# print(nocs.head(10))

#checking for nocs duplicates
# nocs.sort_values(by=["Case Number"])
# print("nocs original length:", len(nocs.index))
# nocs = nocs.drop_duplicates(subset=["Case Number", "EPA Received Date"], keep='first')
# print("nocs no duplicates length:", len(nocs.index))

# merged = subs.merge(nocs, left_on="Case Number", right_on="Case Number", how="inner")
# print("merged count:", len(merged.index))
# print(merged.head(10))

# merged['Source Name'].value_counts().plot(kind='bar')
# test_merged = merged.head(400)

# fig = px.timeline(test_merged, x_start="EPA Received Date_x", x_end="Version Published Date", y="Case Number", color="Source Name")
# fig.show()


# ids = nocs["Case Number"]
# duplicated = nocs[ids.isin(ids[ids.duplicated()])].sort_values("Case Number")
# print(duplicated.head(20))
# merged = subs.merge(pmns, left_on="Case Number", right_on="Case Number", how="inner")

# print("subs count:", len(subs.index))
# print("pmns count:", len(pmns.index))
# print("merged count:", len(merged.index))
# print(merged.head(10))



###
# nots exploration
# import nots
nots.columns
nots.size

# check for duplicates ## no duplicates
#nots = nots.sort_values(by=['Review Start Date'], ascending=[False])
#print("nots original length:", len(nots.index))
#nots = nots.drop_duplicates()
#print("nots no duplicates length:", len(nots.index)) 

## should drop microbial cases ('J-')

#plotting nots timeline
#currently opens browser for interactivity (IDE option available)
test_nots = nots.sample(frac=0.5)
fig = px.timeline(test_nots, x_start='Review Start Date', x_end='Decision Date', y="Case Number")
fig.show()


# how long do these reviews take?
nots['Review Start Date'] = pd.to_datetime(nots['Review Start Date'])
nots['Decision Date'] = pd.to_datetime(nots['Decision Date'])
nots['duration'] = nots['Decision Date'] - nots['Review Start Date']
nots['duration'] = nots['duration'].dt.days.astype('int')
# reviews less than 90 days
nots[nots['duration']<=90].size
# reviews more than 90 days
nots[nots['duration']>90].size

# plot a histogram of timelines
plt.hist(nots['duration'], bins=40)
plt.vlines(90, 0, 200, color='red')
plt.ylim(0, 175)

# pmns - chemview
# check for duplicates 
print("pmns original length:", len(pmns.index))
pmns = pmns.drop_duplicates()
print("pmns no duplicates length:", len(pmns.index)) ## lots of duplicates

# see what happens if we combine case numbers with "A" or other suffixes
pmns['Case Number'] = pmns['Case Number'].map(lambda x: x[0:9]) # this doesn't work for cases with "SN" prefix but is ok for now
pmns['EPA Received Date'] = pd.to_datetime(pmns['EPA Received Date'])
pmns['EPA Approval Date'] = pd.to_datetime(pmns['EPA Approval Date'])

# plot in timeline format with 'Version' as the color
# select a subset of cases with a lot of versions
test_pmns = pmns.sort_values(by='Version', ascending=False).head(75)
fig = px.timeline(test_pmns, x_start="EPA Received Date", x_end="EPA Approval Date", y="Case Number", color="Version")
fig.show()
import plotly.express as px
import pandas as pd
import plotly.io as pio
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






import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Convert DBLP CSV to MLG dividing by year')
parser.add_argument('-s', dest='start_year', default=2016)
parser.add_argument('-e', dest='end_year', default=2022)
parsed_args = parser.parse_args()

# 读解析后的DBLP数据
print("Reading csv...")
to_convert_paper_type = ["output_inproceedings.csv", "output_article.csv"]
df_list = []
for file_name in to_convert_paper_type:
    df = pd.read_csv(file_name, sep=" ", index_col="id")
    df = df[["year", "title", "author"]]
    df_list.append(df)
df = pd.concat(df_list, axis=0)
del df_list

# 形成层与年份对应关系并保存
layer_id = 1
year_to_layer = {}
layer_to_edge_num = {}
for year in range(parsed_args.start_year, parsed_args.end_year + 1):
    year_to_layer[year] = layer_id
    layer_to_edge_num[layer_id] = 0
    layer_id += 1
with open("metainfo_year_layer.txt", "w") as f:
    for year, layer in year_to_layer.items():
        f.write(f"Year {year} in layer {layer}\n")

# 统计author发文数目
print("Counting paper for each author...")
author_name_to_papers = {}
useful_entity = []
for row in df.iterrows():
    # 筛选给定年份的论文
    try:
        year = int(row[1]["year"])
        if year not in year_to_layer:
            continue
        layer_id = year_to_layer[year]
    except:
        continue

    # 提取作者
    try:
        author_list = row[1]["author"].split("|||")
    except:
        continue

    # 对有合作者的论文进行统计
    if len(author_list) > 1:
        for author in author_list:
            try:
                author_name_to_papers[author] += 1
            except KeyError:
                author_name_to_papers[author] = 0
    useful_entity.append(row)

# 筛选发文>1的作者
print("Filtering author...")
total_author_id = 0
author_name_to_id = {}
for author, paper_num in author_name_to_papers.items():
    if paper_num > 1:
        author_name_to_id[author] = total_author_id
        total_author_id += 1

# 保存作者-id关系
with open("metainfo_id_author.txt", "w") as f:
    f.write("ID Author\n")
    for author, author_id in author_name_to_id.items():
        f.write(f"{author_id} {author}\n")

# 根据年份构建MLG
print("Constructing Multilayer Graph...")
f = open("dblp.txt", "w")
total_edge_num = 0
for row in useful_entity:
    # 筛选给定年份的论文
    try:
        year = int(row[1]["year"])
        if year not in year_to_layer:
            continue
        layer_id = year_to_layer[year]
    except:
        continue

    # 提取作者
    try:
        author_list = row[1]["author"].split("|||")
    except:
        continue

    # 建图
    if len(author_list) > 1:
        author_id_list = []
        print(f"{year}-{author_list}")
        for author in author_list:
            try:
                author_id = author_name_to_id[author]
            except KeyError:
                continue
            author_id_list.append(author_id)

        for i in range(0, len(author_id_list)):
            for j in range(i + 1, len(author_id_list)):
                f.write(f"{layer_id} {i} {j}\n")
                total_edge_num += 1
                layer_to_edge_num[layer_id] += 1
f.close()

# 写文件头
with open("dblp.txt", "r+") as f:
    old = f.read()
    f.seek(0)
    f.write(f"{len(year_to_layer)} {total_author_id} {total_edge_num}\n")
    f.write(old)

print(f"NodeNum = {total_author_id}")
print(f"EdgeNum = {layer_to_edge_num}")
print(f"Entities = {len(useful_entity)}")
with open("metainfo.txt", "w") as f:
    f.write(f"Node Num(Author Num) = {total_author_id}\n")
    f.write(f"Each layer edge num = {layer_to_edge_num}")

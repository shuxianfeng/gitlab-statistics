import gitlab
from flask import Flask,render_template,request

app = Flask(__name__,template_folder="templates",static_folder="static")
app.debug=True

gl = gitlab.Gitlab('http://192.168.1.205/',private_token='PQz_5G-ZyqHgQAfbrLdu',timeout=50, api_version='4')

def get_gitlab(t1, t2):
        list2 = []
        projects=gl.projects.list(membership=True, all=True, iterator=True)
        print("时间start:" + t1)
        print("时间end:" + t2)
        for project in projects:
            for branch in project.branches.list(all=True):
                commits=project.commits.list(all=True,query_parameters={'since': t1,'until':t2, 'ref_name': branch.name})
                for commit in commits:
                    # 不统计Merge合并记录
                    # print(commit)
                    if "Merge" in commit.title or "Merge" in commit.message or "合并" in commit.title or "合并" in commit.message:
                        continue

                    com = project.commits.get(commit.id)

                    if com.stats["total"] > 8000:  # 单次提交大于8000行的代码，可能是脚手架之类生成的代码，不做处理
                        continue

                    pro={}
                    try:
                        #print(project.path_with_namespace,com.author_name,com.stats["total"])
                        pro["projectName"]=project.path_with_namespace
                        pro["authorName"]=com.author_name
                        pro["branch"]=branch.name
                        pro["additions"]=com.stats["additions"]
                        pro["deletions"]=com.stats["deletions"]
                        pro["commitNum"]=com.stats["total"]
                        list2.append(pro)
                    except :
                        print("有错误, 请检查")
            print("完成一个项目循环：" + project.path_with_namespace)
        print("完成所有项目统计")
        return list2


@app.route("/", methods = ['GET', 'POST'])
def data():
    if request.method=='GET':
        return  render_template("gitlab.html")
    else:
        ret = {}
        t1 = request.form.get('t1')
        t2 = request.form.get('t2')
        for ele in get_gitlab(t1,t2):
            key = ele["projectName"]+ele["authorName"]+ele["branch"]
            if key not in ret:
                ret[key] = ele
                ret[key]["commitTotal"] = 1
            else:
                ret[key]["additions"] += ele["additions"]
                ret[key]["deletions"] += ele["deletions"]
                ret[key]["commitNum"] += ele["commitNum"]
                ret[key]["commitTotal"] +=1

        list1 = []
        for key,v in ret.items():
            v["项目名"] = v.pop("projectName")
            v["开发者"] = v.pop("authorName")
            v["分支"] = v.pop("branch")
            v["添加代码行数"] = v.pop("additions")
            v["删除代码行数"] = v.pop("deletions")
            v["提交总行数"] = v.pop("commitNum")
            v["提交次数"] = v["commitTotal"]
            list1.append(v)
        #print(list1)

        return render_template("gitlab.html",msg=list1)

   



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8888")
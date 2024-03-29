import sys,pymysql,json
from khan_config import *

class projectinfo:
    def __init__(self,projectID):
        self.projectID = projectID #项目ID
        #定义基础项目类: 
        self.conn = pymysql.connect(**conn_khan)
        self.cursor = self.conn.cursor()

    def get_prj_baseinfo(self):
        """
        Purpose:查询基本信息 
        """
        prj_info = {}
        sql_project = "select id,name,project_key,category,status,liable_user_name,liable_user_account,code_storage,dn_name from kh_project where id={0}".format(self.projectID)
        self.cursor.execute(sql_project)
        result = self.cursor.fetchone()
        #项目基本信息属性
        prj_info['prj_name'] = result[1] #项目名称
        prj_info['prj_ename'] = result[2] #项目英文名称
        prj_info['prj_type'] = project_type[result[3]] #项目类型
        prj_info['prj_status'] = project_status[result[4]] #项目状态
        prj_info['prj_manager_name'] = result[5] #项目经理姓名
        prj_info['prj_manager_ename'] = result[6] #项目经理英文名
        prj_info['prj_codestore'] = code_store[result[7]] #代码存管
        prj_info['prj_dept'] = result[8] #项目归属部门
        return prj_info
    # end def

    def get_prj_codestore(self):
        """
        Purpose: 查询项目代码库信息
        """
        sql_project = '''
        SELECT 
            pr.repository_id '代码库id',
            gr.name '代码库名称',
            gr.http_url_to_repo '代码库地址' 
        FROM 
	        kh_project__repository pr
	        INNER JOIN  kh_gitlab_repository gr on pr.repository_id = gr.id
        WHERE 
	        pr.project_id = {0}'''.format(self.projectID)
        self.cursor.execute(sql_project)
        result = self.cursor.fetchall()
        return result
    
    def get_prj_contract(self):
        """
        Purpose: 查询项目关联合同信息
        """
        sql_project = '''
        SELECT 
            project_id '项目id',
            project_key '项目英文名',
            project_name '项目名称',
            contract_num '合同编号',
            contract_name '合同名称',
            CAST(newlysigned_confirmation AS SIGNED) '新签合同额',
            busi_direc '一级部门',
            dept_name '二级部门',
            province '客户省分',
            custom_direc '客户行业',
            manager '销售经理'
        FROM 
            kh_project_contract
        WHERE 
            project_id = {0}'''.format(self.projectID)
        self.cursor.execute(sql_project)
        result = self.cursor.fetchall()
        return result
    
    def get_prj_commit_by_person(self):
        """
        Purpose: 查询项目关联合同信息
        """
        sql_project = '''
        SELECT
            u.first_dept_name '事业部',
            u.second_dept_name '二级部门',
            u.third_dept_name '三级部门',
            u.name '人员姓名',
            d.committer_username '人员账号',
            p.id '项目ID',
            u.post_label '岗位标签',
            p.`name` '提交项目名称',
            d.repository_id '提交代码库ID',
            bb.cou1 '代码库关联项目数'  ,
            #d.committed_date '提交时间',
            DATE_FORMAT(d.committed_date, '%Y-%m-%d') '提交时间',
            d.additions '新增行数',
            d.deletions '删除行数',
            d.file_total '修改文件总数',
            d.total '总变更行数' 
        FROM
            kh_gitlab_commit_detail d
            LEFT JOIN pmo_user u ON d.committer_username = u.account
            LEFT JOIN kh_project__repository pr ON d.repository_id = pr.repository_id
            LEFT JOIN kh_project p ON pr.project_id = p.id 
            left join (select repository_id,count(project_id) cou1 from kh_project__repository GROUP BY repository_id ) bb on d.repository_id=bb.repository_id
        where 
            p.id = {0} 
            and d.committed_date >= "2024-02-25" 
            AND committed_date <= "2024-03-25" 
            and d.committer_username!='root' '''.format(self.projectID)
        self.cursor.execute(sql_project)
        result = self.cursor.fetchall()
        return result
       
    
    # end def

        # 关闭光标对象
        self.cursor.close()
        self.conn.close()
    
        
checkpr = projectinfo(107)
l1 = checkpr.get_prj_baseinfo()
l2 = checkpr.get_prj_codestore()
l3 = checkpr.get_prj_contract()
l4 = checkpr.get_prj_commit_by_person()

print(json.dumps(l1,indent=4,ensure_ascii=False))
print(json.dumps(l2,indent=4,ensure_ascii=False))
print(json.dumps(l3,indent=4,ensure_ascii=False))
print(json.dumps(l4,indent=4,ensure_ascii=False))
# print(l1)
# print(l2)
# print(l3)
# print(l4)
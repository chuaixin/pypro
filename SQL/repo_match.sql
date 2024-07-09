SELECT
	PV.project_id '项目ID',
	PV.id '版本ID',
	PVD.depend_project_id '依赖产品ID',
	P.name '依赖产品名称',
	PR.repository_id '代码库ID',
	GITR.`name`'代码库名称' 
	
FROM
	kh_project_version PV 
	LEFT JOIN kh_project_version_dependency PVD ON PVD.project_version_id = PV.id
	LEFT JOIN kh_project__repository PR ON PVD.depend_project_id = PR.project_id
	LEFT JOIN kh_gitlab_repository GITR ON GITR.id = PR.repository_id
	LEFT JOIN kh_project p ON PVD.depend_project_id = p.id 

WHERE
	pv.project_id = 1348


SELECT
	PV.project_id '项目ID',
	PV.id '版本ID',
	PR.repository_id '代码库ID',
	GITR.`name`'代码库名称' 
	
FROM
	kh_project_version PV 
	LEFT JOIN kh_project__repository PR ON PV.project_id = PR.project_id
	LEFT JOIN kh_gitlab_repository GITR ON GITR.id = PR.repository_id

WHERE
	pv.project_id = 1348

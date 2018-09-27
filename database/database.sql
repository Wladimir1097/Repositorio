/*===================================================================================================*/
--BORRADO DE LA COMPAÑIA
delete from company_company;
ALTER SEQUENCE company_company_id_seq RESTART WITH 1;
--BORRADO DE TIPOS DE MÓDULOS Y MÓDULOS
delete from security_module;
ALTER SEQUENCE security_module_id_seq RESTART WITH 1;
delete from security_moduletype;
ALTER SEQUENCE security_moduletype_id_seq RESTART WITH 1;
insert into security_moduletype(name,icon,is_active) values('Administración','fa fa-building',True);
insert into security_moduletype(name,icon,is_active) values('Seguridad','fa fa-lock',True);
--INGRESO DE LOS MÓDULOS COMUNES
insert into security_module(url,name,icon,is_active,is_visible,is_vertical,type_id) values('/company/','Administración','fa fa-building',True,True,True,1);
insert into security_module(url,name,icon,is_active,is_visible,is_vertical,type_id) values('/security/module','Módulos','fa fa-gear',True,True,True,2);
insert into security_module(url,name,icon,is_active,is_visible,is_vertical,type_id) values('/security/module_type','Tipos de Módulos','fa fa-bookmark',True,True,True,2);
insert into security_module(url,name,icon,is_active,is_visible,is_vertical,type_id) values('/security/database','Base de Datos','fa fa-database',True,True,True,2);
insert into security_module(url,name,icon,is_active,is_visible,is_vertical,type_id) values('/security/groups','Grupos de Perfiles','fa fa-users',True,True,True,2);
insert into security_module(url,name,icon,is_active,is_visible,is_vertical,type_id) values('/users/','Usuarios','fa fa-user',True,True,True,2);
insert into security_module(url,name,icon,is_active,is_visible,is_vertical,type_id) values('/security/access_users','Accesos de los Usuarios','fa fa-lock',True,True,True,2);
insert into security_module(url,name,icon,is_active,is_visible,is_vertical,type_id) values('/users/change_profile','Edición de Perfil','fa fa-pencil',True,False,False,Null);
insert into security_module(url,name,icon,is_active,is_visible,is_vertical,type_id) values('/company/expenses','Gastos','fa fa-usd',True,True,True,1);
insert into security_module(url,name,icon,is_active,is_visible,is_vertical,type_id) values('/company/type_expense','Tipos de Gastos','fa fa-money',True,True,True,1);
--INGRESO DE LOS GRUPOS
select * from security_module order by id;
delete from auth_group;
ALTER SEQUENCE auth_group_id_seq RESTART WITH 1; 
insert into auth_group(name) values('Administrador');
--INGRESO DE LOS GRUPOS DE MÓDULOS
delete from security_groupmodule;
ALTER SEQUENCE security_groupmodule_id_seq RESTART WITH 1; 
insert into security_groupmodule(groups_id,modules_id) values(1,1);
insert into security_groupmodule(groups_id,modules_id) values(1,2);
insert into security_groupmodule(groups_id,modules_id) values(1,3);
insert into security_groupmodule(groups_id,modules_id) values(1,4);
insert into security_groupmodule(groups_id,modules_id) values(1,5);
insert into security_groupmodule(groups_id,modules_id) values(1,6);
insert into security_groupmodule(groups_id,modules_id) values(1,7);
insert into security_groupmodule(groups_id,modules_id) values(1,8);
insert into security_groupmodule(groups_id,modules_id) values(1,9);
insert into security_groupmodule(groups_id,modules_id) values(1,10);
--INGRESO DE LOS GRUPOS CON EL USUARIO
select * from users_user;
delete from users_user_groups;
ALTER SEQUENCE users_user_groups_id_seq RESTART WITH 1;
insert into users_user_groups(user_id,group_id) values(1,1); 
BORRADO DE COMPRAS Y CREDITOS
================================================================================================*/
delete from sales_devolutionsales;
ALTER SEQUENCE sales_devolutionsales_id_seq RESTART WITH 1; 
delete from sales_salesproducts;
ALTER SEQUENCE sales_salesproducts_id_seq RESTART WITH 1;
delete from sales_salesservices;
ALTER SEQUENCE sales_salesservices_id_seq RESTART WITH 1;
delete from sales;
ALTER SEQUENCE sales_id_seq RESTART WITH 1;
/*
BORRADO DE COMPRAS E INVENTARIOS
================================================================================================*/
delete from ingress_inventory;
ALTER SEQUENCE ingress_inventory_id_seq RESTART WITH 1;
delete from ingress_ingress;
ALTER SEQUENCE ingress_ingress_id_seq RESTART WITH 1;
update ingress_product set stock=0;

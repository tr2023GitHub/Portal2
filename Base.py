import sqlite3

class ProductDB:
    def __init__(self, connect: sqlite3.Connection) -> None:
        self.__connect = connect
        self.__cursor = connect.cursor()
    def getAllProduct(self):
       
        sql ="""SELECT offers.id, offers.name_soft, offers.min_description, companys.name_company, companys.site, companys.logo ,
        offers.id_class, offers.id_industry
        FROM offers 
        INNER JOIN companys on offers.id_company = companys.id 
        INNER JOIN class on offers.id_class = class.id
        INNER JOIN industry on offers.id_industry = industry.id		
        WHERE offers.id = companys.id """
        # тогда не будет выполняться оператор и БД не будет падать !
        try:
            self.__cursor.execute(sql)
            return self.__cursor.fetchall()
        except:
             print("ошибка 1 чтения из базы данных")
             return []
        
    def getProduct(self, id):
        # sql = "SELECT * FROM offers_class_comp_ind_os WHERE id = ?"
        # sql ="SELECT offers.name, offers.trip, offers.data, offers.price, offers.description, offers.img, images.img1, images.img2 FROM offers INNER JOIN images on offers.id = images.id WHERE offers.id= ?"
        #sql ="SELECT offers.name_soft, offers.min_description, offers.max_description, offers.id_class, companys.name_company, companys.site, companys.logo FROM offers INNER JOIN companys on offers.id_company = companys.id WHERE offers.id = ?"
        sql ="""SELECT offers.name_soft, offers.min_description, offers.max_description,offers.id, class.name_class, companys.name_company, companys.site,
                companys.logo, industry.name_ind
                FROM offers_class_comp_ind_os
                JOIN offers ON offers_class_comp_ind_os.offers_id = offers.id
                JOIN class ON offers_class_comp_ind_os.class_id = class.id
                JOIN companys ON offers_class_comp_ind_os.companys_id = companys.id 
                JOIN industry ON offers_class_comp_ind_os.industry_id = industry.id 
                WHERE offers_class_comp_ind_os.offers_id = ?"""
        # sql ="SELECT offers.name_soft, offers.min_description, offers.max_description, class.name, companys.name_company, companys.site, companys.logo FROM offers_class_comp_ind_os JOIN offers ON offers_class_comp_ind_os.offers_id = offers.id JOIN class ON offers_class_comp_ind_os.class_id = class.id JOIN companys ON offers_class_comp_ind_os.companys_id = companys.id WHERE offers_class_comp_ind_os.offers_id = ?"
                
        self.__cursor.execute(sql, tuple([id]))
        return self.__cursor.fetchone()
       
   
     

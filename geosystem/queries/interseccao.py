INSERT_INTERSECCAO = """
BEGIN
    DECLARE
    
    V_VALOR NUMBER;
    V_INTER NUMBER;
    V_JSON1 CLOB;
    V_QUERY CLOB;
    
    BEGIN
    
        V_INTER := %s;
        V_VALOR := %s;
        V_JSON1 := '%s';
                
        V_QUERY := 'INSERT INTO TEMP_INTERSECCAO(INTER, VALOR, GEOM) VALUES(:INTER, :VALOR, JSON_VALUE(:JSON1, ''$'' RETURNING SDO_GEOMETRY))';

        EXECUTE IMMEDIATE V_QUERY USING V_INTER, V_VALOR, V_JSON1;

    END;
    
END;
"""

SELECT_INTERSECCAO = """
    WITH
        JSON AS
            (
                SELECT  A.DESCRICAO
                    ,   A.DATA
                    ,   C.NOME_TALHAO
                    ,   D.GEOM
                    ,   D.DATA_INICIO
                    ,   D.DATA_FIM
                    ,   D.AREA AREA_TALHAO
                    ,   E.INTER
                    ,   E.VALOR
                    ,   E.GEOM INTER_GEOM
                    ,   ROUND(SDO_GEOM.SDO_AREA(E.GEOM)/10000,5) AREA_INTER
                    ,   F.DESCRICAO NOME_ATRIBUTO
                FROM INTERPOLACAO_CADASTRO A
                JOIN INTERPOLACAO_ABRANGENCIA B ON(A.ID = B.INTERPOLACAO_ID)
                JOIN TALHAO_CADASTRO C ON(C.ID = B.TALHAO_ID)
                JOIN TALHAO_GEOM D ON(D.TALHAO_CAD_ID = C.ID)
                JOIN TEMP_INTERSECCAO E ON(A.ID = E.INTER)
                JOIN ATRIBUTO_CADASTRO F ON(A.ATRIBUTO_ID = F.ID)
            )
    SELECT  DESCRICAO
--        ,   DATA
        ,   NOME_TALHAO
        ,   NOME_ATRIBUTO
        ,   VALOR
--        ,   SDO_RELATE(INTER_GEOM, GEOM, 'mask=INSIDE') RELATE
        ,   CASE WHEN SDO_UTIL.TO_WKTGEOMETRY(SDO_GEOM.SDO_INTERSECTION(INTER_GEOM, GEOM, .005)) IS NULL 
                THEN  SDO_UTIL.TO_WKTGEOMETRY(INTER_GEOM)
                ELSE  SDO_UTIL.TO_WKTGEOMETRY(SDO_GEOM.SDO_INTERSECTION(INTER_GEOM, GEOM, .005))
            END GEOM
    FROM JSON A
    WHERE DATA BETWEEN DATA_INICIO AND NVL(DATA_FIM, SYSDATE)
        AND SDO_RELATE(INTER_GEOM, GEOM, 'mask=ANYINTERACT') = 'TRUE'
 
"""

LOTE_TALHAO = """
    SELECT
            B.TALHAO_ID 
        ,   TO_CHAR(A.DATA, 'DD/MM/YYYY') DATA
    FROM INTERPOLACAO_CADASTRO A
    JOIN INTERPOLACAO_ABRANGENCIA B ON(A.ID = B.INTERPOLACAO_ID)
    WHERE A.ID = %s
"""

SELECT_LOTE_INT = """
    SELECT  B.PONTO_COLETA  ID_AMOSTRA
        ,   A.DESCRICAO     NOME_LOTE
        ,   A.DATA          DATA
        ,   B.ATRIBUTO      DESCRICAO_ATRIBUTO
        ,   B.VALOR
        ,   B.LATITUDE
        ,   B.LONGITUDE
    FROM INTERPOLACAO_LOTE A
    JOIN INTERPOLACAO_LOTE_PONTOS B ON(A.ID = B.INTERPOLACAO_LOTE_ID)
    WHERE PROCESSADO = 0
        AND A.ID = %s
        AND B.ATRIBUTO_ID = %s
        ORDER BY B.PONTO_COLETA 
"""

SELECT_LOTE_DATA = """
    SELECT  TO_CHAR(A.DATA_CADASTRO, 'DD/MM/YYYY') DATA_CADASTRO
    FROM LOTE_CADASTRO A
    WHERE A.ID = %s
"""

LOTE_INDEX = """
    WITH
        REL1 AS
            (
                SELECT  DISTINCT
                        A.ID LOTE_ID
                    ,   A.DESCRICAO
                    ,   TO_CHAR(A.DATA, 'YYYY-MM-DD') AS DATA
                    ,   C.ID ATRIBUTO_ID
                    ,   C.DESCRICAO ATRIBUTO_CADASTRO
                    ,   B.ATRIBUTO ATRIBUTO_ORIGEM
                    ,   B.PROCESSADO
                FROM INTERPOLACAO_LOTE A
                JOIN INTERPOLACAO_LOTE_PONTOS B ON(A.ID = B.INTERPOLACAO_LOTE_ID)
                LEFT JOIN ATRIBUTO_CADASTRO C ON(B.ATRIBUTO_ID = C.ID)
                WHERE A.ID    BETWEEN (CASE WHEN TO_NUMBER(%s) = 0 THEN 0 ELSE TO_NUMBER(%s) END)
                    AND (CASE WHEN TO_NUMBER(%s) = 0 THEN 99999999 ELSE TO_NUMBER(%s) END)
                AND TO_CHAR(B.PROCESSADO) LIKE (CASE   
                                                    WHEN %s = 1 THEN '1'
                                                    WHEN %s = 2 THEN '%%'
                                                ELSE '0' END)
            )
    SELECT JSON_OBJECT(*) JSON FROM REL1
"""

LOTE_INDEX_NULL = """
    WITH
        REL1 AS
            (
                SELECT  DISTINCT
                        A.ID LOTE_ID
                    ,   A.DESCRICAO
                    ,   TO_CHAR(A.DATA, 'YYYY-MM-DD') AS DATA
                    ,   C.ID ATRIBUTO_ID
                    ,   C.DESCRICAO ATRIBUTO_CADASTRO
                    ,   B.ATRIBUTO ATRIBUTO_ORIGEM
                    ,   B.PROCESSADO
                FROM INTERPOLACAO_LOTE A
                JOIN INTERPOLACAO_LOTE_PONTOS B ON(A.ID = B.INTERPOLACAO_LOTE_ID)
                LEFT JOIN ATRIBUTO_CADASTRO C ON(B.ATRIBUTO_ID = C.ID) 
                WHERE PROCESSADO = 0
                AND A.ID    BETWEEN (CASE WHEN TO_NUMBER(%s) = 0 THEN 0 ELSE TO_NUMBER(%s) END)
                    AND (CASE WHEN TO_NUMBER(%s) = 0 THEN 99999999 ELSE TO_NUMBER(%s) END)
                AND C.ID IS NOT NULL
                AND TO_CHAR(B.PROCESSADO) LIKE (CASE   
                                                    WHEN %s = 1 THEN '1'
                                                    WHEN %s = 2 THEN '%%'
                                                ELSE '0' END)
            )
    SELECT JSON_OBJECT(*) JSON FROM REL1
"""

INSERT_LOTE_PONTOS = """
    INSERT INTO INTERPOLACAO_LOTE_PONTOS(INTERPOLACAO_LOTE_ID, ATRIBUTO, PONTO_COLETA, LATITUDE, LONGITUDE, VALOR, ATRIBUTO_ID)
    WITH
        SEL AS
        (
            SELECT  %s INTERPOLACAO_LOTE_ID
                ,  '%s' ATRIBUTO
                ,   %s PONTO_COLETA
                ,   %s LATITUDE
                ,   %s LONGITUDE
                ,   %s VALOR
            FROM DUAL
        )
        SELECT  A.INTERPOLACAO_LOTE_ID
            ,   A.ATRIBUTO
            ,   A.PONTO_COLETA
            ,   A.LATITUDE
            ,   A.LONGITUDE
            ,   A.VALOR
            ,   B.ATRIBUTO_ID
        FROM SEL A
        LEFT JOIN ATRIBUTO_ALIAS B ON(A.ATRIBUTO = B.NOME_ALIAS)    
"""

SELECT_LOTE = """
SELECT  A.ID LOTE_ID
    ,   A.NOME_LOTE
    ,   A.DATA_CADASTRO
    ,   B.DESCRICAO_ATRIBUTO
    ,   D.NOME_TALHAO
    ,   B.VALOR
    ,   C.GEOM
FROM LOTE_CADASTRO A
JOIN LOTE_ATRIBUTO B ON(A.ID = B.LOTE_ID)
JOIN LOTE_GEOM C ON(A.ID = C.LOTE_ID AND B.LOTE_ID = C.LOTE_ID AND B.ID_AMOSTRA = C.ID_AMOSTRA)
JOIN TALHAO_CADASTRO D ON(B.TALHAO_ID = D.ID)
WHERE DESCRICAO_ATRIBUTO = '%s'
"""

INSERT_LOTE_GEOM = """
    INSERT INTO LOTE_GEOM(LOTE_ID, ID_AMOSTRA, GEOM)
    VALUES (%s, %s, JSON_VALUE('%s', '$' RETURNING SDO_GEOMETRY))
"""


INSERT_LOTE = """
    INSERT INTO LOTE_ATRIBUTO(LOTE_ID, TALHAO_ID, ATRIBUTO_ID, ID_AMOSTRA, ATRIBUTO_ORIGEM, VALOR)
    VALUES (%s, %s, %s, %s, '%s', %s)
"""

LOTE_ABRANGENCIA = """
WITH
    REL1 AS
        (
            SELECT  D.ID
                ,   D.NOME_TALHAO AS TALHAO
                ,   E.NOME_FAZENDA
                ,   MDSYS.SDO_GEOMETRY(2001, 4326, SDO_POINT_TYPE(LONGITUDE, LATITUDE, NULL), NULL, NULL) GEOM_PONTO
                ,   C.GEOM
            FROM INTERPOLACAO_LOTE A
            JOIN INTERPOLACAO_LOTE_PONTOS B ON(A.ID = B.INTERPOLACAO_LOTE_ID)
            CROSS JOIN TALHAO_GEOM C
            JOIN TALHAO_CADASTRO D ON(D.ID = C.TALHAO_CAD_ID)
            JOIN TALHAO_FAZENDA E ON(E.ID = D.FAZENDA_ID)
            WHERE INTERPOLACAO_LOTE_ID = %s
                AND ATRIBUTO_ID = %s
                AND A.DATA BETWEEN C.DATA_INICIO AND NVL(C.DATA_FIM, SYSDATE)
                AND C.VALIDO = 1
        )
        SELECT  ID TALHAO_ID
            ,   TALHAO
            ,   NOME_FAZENDA
            ,   COUNT(1) QUANTIDADE_PONTOS
        FROM REL1
        WHERE SDO_RELATE(GEOM_PONTO, GEOM, 'mask=anyinteract') = 'TRUE'
        GROUP BY   ID
            ,   TALHAO
            ,   NOME_FAZENDA
"""

INSERT_INTER_LOTE = """
INSERT INTO INTERPOLACAO_GEOM(INTERPOLACAO_ID, VALOR, GEOM)
SELECT %s, "valor", GEOM FROM %s
"""


LOTE_AUTO = """
WITH
    SEL AS
        (
            SELECT  DISTINCT
                    A.ID
                ,   A.DESCRICAO
                ,   TO_CHAR(A.DATA, 'DD-MM-YYYY') DATA
                ,   A.TIPO_INTERPOLACAO_ID TIPO_ID
                ,   B.ATRIBUTO_ID
            FROM INTERPOLACAO_LOTE A
            JOIN INTERPOLACAO_LOTE_PONTOS B ON (A.ID = B.INTERPOLACAO_LOTE_ID)
            WHERE B.ATRIBUTO_ID IS NOT NULL
                AND A.ID = %s
                AND B.PROCESSADO = 0
                ORDER BY ATRIBUTO_ID
        )
    SELECT JSON_OBJECT(*) JSON_SEL FROM SEL
"""

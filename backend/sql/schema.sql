CREATE TABLE IF NOT EXISTS usuario (
    id_usuario  SERIAL PRIMARY KEY,
    nome        VARCHAR(100) NOT NULL,
    email       VARCHAR(255) NOT NULL UNIQUE,   
    senha       VARCHAR(255) NOT NULL           
);

CREATE TABLE IF NOT EXISTS registro (
    id_registro     SERIAL PRIMARY KEY,
    data_hora       TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    tipo            VARCHAR(10) NOT NULL,
    conteudo_texto  TEXT NOT NULL,             
    id_usuario      INTEGER NOT NULL REFERENCES usuario (id_usuario) ON DELETE CASCADE,  
    CONSTRAINT ck_registro_tipo CHECK (tipo IN ('texto', 'voz'))                         
);

CREATE TABLE IF NOT EXISTS analise (
    id_analise              SERIAL PRIMARY KEY,
    data_analise            TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    sentimento              VARCHAR(10) NOT NULL,      
    categoria_predominante  VARCHAR(20),
    contexto                VARCHAR(20),               
    categorias              VARCHAR(20)[] NOT NULL,    
    resumo                  TEXT NOT NULL,
    modelo                  VARCHAR(100) NOT NULL,     
    id_registro             INTEGER NOT NULL UNIQUE    
                            REFERENCES registro (id_registro) ON DELETE CASCADE  
);
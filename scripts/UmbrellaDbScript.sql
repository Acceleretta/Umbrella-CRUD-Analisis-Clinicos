create table if not exists estudio
(
    Id_Estudio   int auto_increment
        primary key,
    Nombre       varchar(50)     not null,
    Precio       double unsigned not null,
    Rango_Inicio int             null,
    Rango_Fin    int             null
);

create definer = root@localhost trigger tr_cambio_precio
    after update
    on estudio
    for each row
BEGIN
    insert into cambio_precio (Id_Estudio, Precio_Anterior, Fecha_Cambio, Precio_Nuevo)
    values (OLD.Id_Estudio, OLD.Precio, NOW(), NEW.Precio);
END;

create definer = root@localhost trigger tr_cambio_rango
    after update
    on estudio
    for each row
BEGIN
    insert into cambio_rango (Id_Estudio, Rango_Inicio_Anterior, Rango_Fin_Anterior, Rango_Inicio_Nuevo,
                              Rango_Fin_Nuevo, Fecha_Cambio)
    values (OLD.Id_Estudio, OLD.Rango_Inicio, OLD.Rango_Fin, NEW.Rango_Inicio, NEW.Rango_Fin, NOW());
END;


create table if not exists cliente
(
    Id_Cliente       int auto_increment
        constraint `PRIMARY`
        primary key,
    Nombre           varchar(50) not null,
    Ap_Paterno       varchar(50) not null,
    Ap_Materno       varchar(50) not null,
    Fecha_Nacimiento date        null,
    Telefono         varchar(10) null,
    Correo           varchar(50) null
);

create table if not exists estudio
(
    Id_Estudio   int auto_increment
        constraint `PRIMARY`
        primary key,
    Nombre       varchar(50)     not null,
    Precio       double unsigned not null,
    Rango_Inicio int             null,
    Rango_Fin    int             null
);

create table if not exists cambio_precio
(
    Id_Cambio_Precio int auto_increment
        constraint `PRIMARY`
        primary key,
    Id_Estudio       int             not null,
    Precio_Anterior  double unsigned null,
    Precio_Nuevo     double unsigned null,
    Fecha_Cambio     date            not null,
    constraint Cambio_Precio_estudio_Id_Estudio_fk
        foreign key (Id_Estudio) references estudio (Id_Estudio)
);

create table if not exists cambio_rango
(
    Id_Cambio_Rango       int auto_increment
        constraint `PRIMARY`
        primary key,
    Id_Estudio            int  not null,
    Rango_Inicio_Anterior int  null,
    Rango_Fin_Anterior    int  null,
    Rango_Inicio_Nuevo    int  null,
    Rango_Fin_Nuevo       int  null,
    Fecha_Cambio          date null,
    constraint cambio_rango_estudio_Id_Estudio_fk
        foreign key (Id_Estudio) references estudio (Id_Estudio)
);

create trigger tr_cambio_precio
    after update
    on estudio
    for each row
BEGIN
    insert into cambio_precio (Id_Estudio, Precio_Anterior, Fecha_Cambio, Precio_Nuevo)
    values (OLD.Id_Estudio, OLD.Precio, NOW(), NEW.Precio);
END;

create trigger tr_cambio_rango
    after update
    on estudio
    for each row
BEGIN
    insert into cambio_rango (Id_Estudio, Rango_Inicio_Anterior, Rango_Fin_Anterior, Rango_Inicio_Nuevo,
                              Rango_Fin_Nuevo, Fecha_Cambio)
    values (OLD.Id_Estudio, OLD.Rango_Inicio, OLD.Rango_Fin, NEW.Rango_Inicio, NEW.Rango_Fin, NOW());
END;

create table if not exists orden_analisis
(
    Id_Orden_Analisis int auto_increment
        constraint `PRIMARY`
        primary key,
    Id_Cliente        int      not null,
    Fecha             datetime not null,
    constraint orden_analisis_cliente_Id_Cliente_fk
        foreign key (Id_Cliente) references cliente (Id_Cliente)
);

create table if not exists detalle_orden
(
    Id_Detalle_Orden  int auto_increment
        constraint `PRIMARY`
        primary key,
    Id_Orden_Analisis int not null,
    Id_Estudio        int not null,
    constraint detalle_orden_estudio_id_estudio_fk
        foreign key (Id_Estudio) references estudio (Id_Estudio),
    constraint detalle_orden_id_orden_analisis_Id_Orden_Analisis_fk
        foreign key (Id_Orden_Analisis) references orden_analisis (Id_Orden_Analisis)
);

create table if not exists factura
(
    Id_Factura        int auto_increment
        constraint `PRIMARY`
        primary key,
    Id_Orden_Analisis int    null,
    Fecha             date   not null,
    Monto             double not null,
    Razon             text   null,
    constraint Factura_detalle_orden_Id_Orden_Analisis_fk
        foreign key (Id_Orden_Analisis) references detalle_orden (Id_Orden_Analisis)
);

create table if not exists resultado_analisis
(
    Id_Resultado_Analisis int auto_increment
        constraint `PRIMARY`
        primary key,
    Id_Detalle_Orden      int      null,
    Valor                 int      not null,
    Fecha                 datetime null,
    constraint resultado_analisis_detalle_orden_Id_Detalle_Orden_fk
        foreign key (Id_Detalle_Orden) references detalle_orden (Id_Detalle_Orden)
);

create table if not exists cambio_resultado
(
    Id_Cambio_Resultado   int auto_increment
        constraint `PRIMARY`
        primary key,
    Id_Resultado_Analisis int  not null,
    Valor_Anterior        int  null,
    Valor_Nuevo           int  null,
    Fecha_Cambio          date null,
    constraint Cambio_Resultado_resultado_analisis_Id_Resultado_Analisis_fk
        foreign key (Id_Resultado_Analisis) references resultado_analisis (Id_Resultado_Analisis)
);

create trigger tr_cambio_resultado
    after update
    on resultado_analisis
    for each row
BEGIN
    insert into cambio_resultado (Id_Resultado_Analisis, Valor_Anterior, Valor_Nuevo, Fecha_Cambio)
    values (OLD.Id_Resultado_Analisis, OLD.Valor, NEW.Valor, NOW());
END;

create view vista_cambio_precio as
select `cp`.`Id_Cambio_Precio` AS `Id_Cambio_Precio`,
       `e`.`Nombre`            AS `Nombre_Estudio`,
       `cp`.`Precio_Anterior`  AS `Precio_Anterior`,
       `cp`.`Precio_Nuevo`     AS `Precio_Nuevo`,
       `cp`.`Fecha_Cambio`     AS `Fecha_Cambio`
from (`umbrelladb`.`cambio_precio` `cp` join `umbrelladb`.`estudio` `e` on ((`cp`.`Id_Estudio` = `e`.`Id_Estudio`)));

create view vista_cambio_rango as
select `cr`.`Id_Cambio_Rango`       AS `Id_Cambio_Rango`,
       `e`.`Nombre`                 AS `Nombre_Estudio`,
       `cr`.`Rango_Inicio_Anterior` AS `Rango_Inicio_Anterior`,
       `cr`.`Rango_Fin_Anterior`    AS `Rango_Fin_Anterior`,
       `cr`.`Rango_Inicio_Nuevo`    AS `Rango_Inicio_Nuevo`,
       `cr`.`Rango_Fin_Nuevo`       AS `Rango_Fin_Nuevo`,
       `cr`.`Fecha_Cambio`          AS `Fecha_Cambio`
from (`umbrelladb`.`cambio_rango` `cr` join `umbrelladb`.`estudio` `e` on ((`cr`.`Id_Estudio` = `e`.`Id_Estudio`)));

create view vista_cambio_resultado as
select `cr`.`Id_Cambio_Resultado` AS `Id_Cambio_Resultado`,
       `oa`.`Id_Orden_Analisis`   AS `Id_Orden_Analisis`,
       `cr`.`Valor_Anterior`      AS `Valor_Anterior`,
       `cr`.`Valor_Nuevo`         AS `Valor_Nuevo`,
       `cr`.`Fecha_Cambio`        AS `Fecha_Cambio`
from (((`umbrelladb`.`cambio_resultado` `cr` join `umbrelladb`.`resultado_analisis` `ra`
        on ((`cr`.`Id_Resultado_Analisis` = `ra`.`Id_Detalle_Orden`))) join `umbrelladb`.`detalle_orden` `do`
       on ((`ra`.`Id_Detalle_Orden` = `do`.`Id_Detalle_Orden`))) join `umbrelladb`.`orden_analisis` `oa`
      on ((`do`.`Id_Orden_Analisis` = `oa`.`Id_Orden_Analisis`)));

create view vista_ordenes_sin_resultados as
select `o`.`Id_Orden_Analisis` AS `Id_Orden_Analisis`,
       `o`.`Id_Cliente`        AS `Id_Cliente`,
       `o`.`Fecha`             AS `Fecha`,
       `d`.`Id_Detalle_Orden`  AS `Id_Detalle_Orden`
from ((`umbrelladb`.`orden_analisis` `o` left join `umbrelladb`.`detalle_orden` `d`
       on ((`o`.`Id_Orden_Analisis` = `d`.`Id_Orden_Analisis`))) left join `umbrelladb`.`resultado_analisis` `r`
      on ((`d`.`Id_Detalle_Orden` = `r`.`Id_Detalle_Orden`)))
where (`r`.`Id_Resultado_Analisis` is null);

create view vista_resultados_con_rango as
select `r`.`Id_Resultado_Analisis`                                                                           AS `Id_Resultado_Analisis`,
       `c`.`Id_Cliente`                                                                                      AS `Id_Cliente`,
       `c`.`Nombre`                                                                                          AS `Nombre`,
       `c`.`Ap_Paterno`                                                                                      AS `Ap_Paterno`,
       `c`.`Ap_Materno`                                                                                      AS `Ap_Materno`,
       `oa`.`Id_Orden_Analisis`                                                                              AS `Id_Orden_Analisis`,
       `r`.`Valor`                                                                                           AS `Valor`,
       `r`.`Fecha`                                                                                           AS `Fecha`,
       `e`.`Rango_Inicio`                                                                                    AS `Rango_Inicio`,
       `e`.`Rango_Fin`                                                                                       AS `Rango_Fin`,
       if((`r`.`Valor` between `e`.`Rango_Inicio` and `e`.`Rango_Fin`), 'Dentro de rango',
          'Fuera de rango')                                                                                  AS `Estado_Rango`
from ((((`umbrelladb`.`cliente` `c` join `umbrelladb`.`orden_analisis` `oa`
         on ((`c`.`Id_Cliente` = `oa`.`Id_Cliente`))) join `umbrelladb`.`detalle_orden` `do`
        on ((`oa`.`Id_Orden_Analisis` = `do`.`Id_Orden_Analisis`))) join `umbrelladb`.`estudio` `e`
       on ((`do`.`Id_Estudio` = `e`.`Id_Estudio`))) join `umbrelladb`.`resultado_analisis` `r`
      on ((`do`.`Id_Detalle_Orden` = `r`.`Id_Detalle_Orden`)));

create procedure sp_actualizar_cliente(IN idCliente int, IN nombreCliente varchar(50),
                                       IN apellidoPatCliente varchar(50), IN apellidoMatCliente varchar(50),
                                       IN nacimientoCliente date, IN telefonoCliente varchar(10),
                                       IN correoCliente varchar(50))
BEGIN
    UPDATE cliente
    SET Nombre           = nombreCliente,
        Ap_Paterno       = apellidoPatCliente,
        Ap_Materno       = apellidoMatCliente,
        Fecha_Nacimiento = nacimientoCliente,
        Telefono         = telefonoCliente,
        Correo           = correoCliente
    WHERE Id_Cliente = idCliente;
END;

create procedure sp_actualizar_estudio(IN idEstudio int, IN nombreEstudio varchar(50), IN costoEstudio double unsigned,
                                       IN rangoIncioEstudio int, IN rangoFinEstudio int)
BEGIN
    UPDATE estudio
    SET Nombre       = nombreEstudio,
        Precio       = costoEstudio,
        Rango_Inicio = rangoIncioEstudio,
        Rango_Fin    = rangoFinEstudio
        WHERE Id_Estudio = idEstudio;
END;

create procedure sp_actualizar_resultado(IN idResultadoAnalisis int, IN idDetalleOrden int, IN valorResultado int)
BEGIN
    UPDATE resultado_analisis
    SET Id_Detalle_Orden = idDetalleOrden,
        Valor            = valorResultado,
        Fecha            = NOW()
    WHERE Id_Resultado_Analisis = idResultadoAnalisis;
END;

create procedure sp_borrar_cliente(IN idCliente int)
BEGIN
    DELETE FROM cliente WHERE Id_Cliente = idCliente;
END;

create procedure sp_borrar_estudio(IN idEstudio int)
BEGIN
    DELETE FROM estudio WHERE Id_Estudio = idEstudio;
END;

create procedure sp_buscar_clientes(IN nombreCliente varchar(50), IN apellidoPatCliente varchar(50),
                                    IN apellidoMatCliente varchar(50))
BEGIN
    SELECT * FROM cliente WHERE nombre LIKE CONCAT('%', nombreCliente, '%');
END;

create procedure sp_crear_factura(IN razonFactura text)
BEGIN
    DECLARE exit handler for sqlexception
        BEGIN
            ROLLBACK;
        END;

    START TRANSACTION;

    -- Obtener el último ID de orden_analisis
    SET @ordenId = (SELECT MAX(Id_Orden_Analisis) FROM orden_analisis);

    -- Verificar si la orden existe
    IF @ordenId IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No hay órdenes disponibles para generar factura';
        ROLLBACK;
    END IF;

    -- Calcular el monto total de la factura
    SET @MontoTotal = (SELECT SUM(E.Precio)
                       FROM detalle_orden D
                                JOIN Estudio E ON D.Id_Estudio = E.Id_Estudio
                       WHERE D.Id_Orden_Analisis = @ordenId);

    -- Insertar la factura
    INSERT INTO factura (Id_Orden_Analisis, Fecha, Monto, Razon)
    VALUES (@ordenId, NOW(), @MontoTotal, razonFactura);

    COMMIT;
END;

create procedure sp_crear_resultado(IN valorResultado int, IN idDetalleOrden int)
BEGIN
    INSERT INTO resultado_analisis (Id_Detalle_Orden, Valor, Fecha)
    VALUES (idDetalleOrden, valorResultado, NOW());
END;

create procedure sp_generar_orden(IN idCliente int, IN idEstudio int)
BEGIN
    DECLARE idOrden INT;
    -- Generar Orden de Análisis
    INSERT INTO orden_analisis (Id_Cliente, Fecha)
    VALUES (idCliente, NOW());

-- Obtener OrdenID de la orden recién generada
    SET idOrden = LAST_INSERT_ID();

-- Agregar estudio a la orden
    INSERT INTO detalle_orden (Id_Orden_Analisis, Id_Estudio)
    VALUES (idOrden, idEstudio);
END;

create procedure sp_insertar_cliente(IN nombreCliente varchar(50), IN apellidoPatCliente varchar(50),
                                     IN apellidoMatCliente varchar(50), IN nacimientoCliente date,
                                     IN telefonoCliente varchar(10), IN correoCliente varchar(50))
BEGIN
    INSERT INTO Cliente (Nombre, Ap_Paterno, Ap_Materno, Fecha_Nacimiento, Telefono, Correo)
    VALUES (nombreCliente, apellidoPatCliente, apellidoMatCliente, nacimientoCliente, telefonoCliente,
            correoCliente);
END;

create procedure sp_insertar_estudio(IN nombreEstudio varchar(50), IN costoEstudio double unsigned,
                                     IN rangoIncioEstudio int, IN rangoFinEstudio int)
BEGIN
    INSERT INTO estudio (Nombre, Precio, Rango_Inicio, Rango_Fin)
    VALUES (nombreEstudio, costoEstudio, rangoIncioEstudio, rangoFinEstudio);
END;

create procedure sp_obtener_cliente()
BEGIN
    SELECT * from cliente;

END;

create procedure sp_obtener_cliente_id(IN idCliente int)
BEGIN
    SELECT * from cliente WHERE Id_Cliente = idCliente;
END;

create procedure sp_obtener_estudio()
BEGIN
    SELECT * FROM estudio;
END;

create procedure sp_obtener_estudio_id(IN idEstudio int)
BEGIN
    SELECT * from estudio WHERE Id_Estudio = idEstudio;
END;

create procedure sp_obtener_facturas()
BEGIN
    SELECT * FROM factura;
END;

create procedure sp_obtener_historial_precios()
BEGIN
    SELECT * FROM vista_cambio_precio;
END;

create procedure sp_obtener_historial_rangos()
BEGIN
    SELECT * FROM vista_cambio_rango;
END;

create procedure sp_obtener_historial_resultados()
BEGIN
    SELECT * FROM vista_cambio_resultado;
END;

create procedure sp_obtener_ordenes_sin_resultados()
BEGIN
    SELECT * FROM vista_ordenes_sin_resultados;
END;

create procedure sp_obtener_resultado_id_orden(IN idResultado int)
BEGIN
    SELECT *
    FROM vista_resultados_con_rango
    where Id_Resultado_Analisis = idResultado;
END;

create procedure sp_obtener_resultados()
BEGIN
    SELECT * FROM resultado_analisis;
END;

create procedure sp_obtener_resultados_id(IN idResultado int)
BEGIN
    SELECT * from resultado_analisis WHERE Id_Resultado_Analisis = idResultado;
END;

create procedure sp_registrar_cliente_generar_orden(IN nombreCliente varchar(50), IN apellidoPatCliente varchar(50),
                                                    IN apellidoMatCliente varchar(50), IN nacimientoCliente date,
                                                    IN telefonoCliente varchar(10), IN correoCliente varchar(50),
                                                    IN nombreEstudio varchar(50))
BEGIN
    DECLARE ClienteExistente INT;

    -- Registrar Cliente
    SELECT Id_Cliente
    INTO ClienteExistente
    FROM cliente
    WHERE Nombre = nombreCliente
      AND Ap_Paterno = apellidoPatCliente
      AND Ap_Materno = apellidoMatCliente
      AND Fecha_Nacimiento = nacimientoCliente;
    IF ClienteExistente IS NULL THEN
        call sp_insertar_cliente(nombreCliente, apellidoPatCliente, apellidoMatCliente, nacimientoCliente,
                                 telefonoCliente,
                                 correoCliente);
        SET ClienteExistente = LAST_INSERT_ID();
    END IF;

-- Obtener ClienteID del cliente recién registrado
    SET @ClienteID = LAST_INSERT_ID();

-- Obtener EstudioID del estudio solicitado
    SET @EstudioID = (SELECT Id_Estudio
                      FROM Estudio
                      WHERE Nombre = nombreEstudio);

-- Generar Orden de Análisis
    INSERT INTO orden_analisis (Id_Cliente, Fecha)
    VALUES (@ClienteID, NOW());

-- Obtener OrdenID de la orden recién generada
    SET @OrdenID = LAST_INSERT_ID();

-- Agregar estudio a la orden
    INSERT INTO detalle_orden (Id_Orden_Analisis, Id_Estudio)
    VALUES (@OrdenID, @EstudioID);
END;


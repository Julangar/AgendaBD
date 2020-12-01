-- phpMyAdmin SQL Dump
-- version 5.0.3
-- https://www.phpmyadmin.net/
--
-- Servidor: db
-- Tiempo de generación: 01-12-2020 a las 20:19:32
-- Versión del servidor: 8.0.22
-- Versión de PHP: 7.4.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `agenda`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `citas`
--

CREATE TABLE `citas` (
  `cit_id` int NOT NULL COMMENT 'identificador de la cita',
  `con_id` int NOT NULL COMMENT 'identificador del contacto',
  `cit_lugar` text NOT NULL COMMENT 'lugar de la cita',
  `cit_fecha` date NOT NULL COMMENT 'fecha de la cita',
  `cit_hora` time NOT NULL COMMENT 'hora de la cita',
  `cit_descripcion` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='tabla de las citas con los contactos';

--
-- Volcado de datos para la tabla `citas`
--

INSERT INTO `citas` (`cit_id`, `con_id`, `cit_lugar`, `cit_fecha`, `cit_hora`, `cit_descripcion`) VALUES
(3, 1, 'Lab 505', '2020-12-15', '14:00:00', 'Entrega de notas'),
(4, 3, 'coordinación pc', '2020-12-10', '10:00:00', 'Entrega carta materias de posgrado'),
(5, 2, 'biblioteca', '2020-12-20', '14:00:00', 'Entrega de trabajo de grado');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `contactos`
--

CREATE TABLE `contactos` (
  `con_id` int NOT NULL COMMENT 'identificador del contacto',
  `usu_id` int NOT NULL,
  `con_nombre` varchar(50) NOT NULL COMMENT 'nombre del contacto',
  `con_apellido` varchar(50) NOT NULL COMMENT 'apellido del contacto',
  `con_direccion` varchar(250) NOT NULL COMMENT 'dirección del contacto',
  `con_telefono` varchar(20) NOT NULL COMMENT 'teléfono del contacto',
  `con_email` varchar(25) NOT NULL COMMENT 'correo electrónico del contacto'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='tabla de los contactos de la agenda';

--
-- Volcado de datos para la tabla `contactos`
--

INSERT INTO `contactos` (`con_id`, `usu_id`, `con_nombre`, `con_apellido`, `con_direccion`, `con_telefono`, `con_email`) VALUES
(1, 1, 'Juan Miguel', 'Diaz Perez', 'Calle 3ra 20-50 ', '3124565656', 'jmiguel@mail.com'),
(2, 1, 'Ana Juliana', 'Hernandez Riaño', 'Autonorte 170-34', '3115434343', 'ajuliana@mail.com'),
(3, 3, 'Pedro ', 'Parrado', 'trans 34 56-97', '3117898989', 'pparrado@mail.com'),
(4, 3, 'José', 'Higuera', 'Trans 12 67-98', '3145678900', 'jhiguera@mail.com');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `usu_id` int NOT NULL,
  `usu_nombre` varchar(30) NOT NULL,
  `usu_clave` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`usu_id`, `usu_nombre`, `usu_clave`) VALUES
(1, 'admin', 'd033e22ae348aeb5660fc2140aec35850c4da997'),
(2, 'usuario1', 'ada6d34bca926b40be00893cabc0aeae138ea2a0'),
(3, 'usuario3', 'cd016c515962508538b851783fee065726058a4a'),
(4, 'usuario2', '515ab0557a960be2bcc227943c20de357fb5672d');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `citas`
--
ALTER TABLE `citas`
  ADD PRIMARY KEY (`cit_id`),
  ADD KEY `fk_citas_contactos` (`con_id`);

--
-- Indices de la tabla `contactos`
--
ALTER TABLE `contactos`
  ADD PRIMARY KEY (`con_id`),
  ADD KEY `fk_contactos_usuarios` (`usu_id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`usu_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `citas`
--
ALTER TABLE `citas`
  MODIFY `cit_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador de la cita', AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `contactos`
--
ALTER TABLE `contactos`
  MODIFY `con_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador del contacto', AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `usu_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `citas`
--
ALTER TABLE `citas`
  ADD CONSTRAINT `fk_citas_contactos` FOREIGN KEY (`con_id`) REFERENCES `contactos` (`con_id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Filtros para la tabla `contactos`
--
ALTER TABLE `contactos`
  ADD CONSTRAINT `fk_contactos_usuarios` FOREIGN KEY (`usu_id`) REFERENCES `usuarios` (`usu_id`) ON DELETE RESTRICT ON UPDATE RESTRICT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

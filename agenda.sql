-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 24-11-2020 a las 20:39:39
-- Versión del servidor: 10.4.16-MariaDB
-- Versión de PHP: 7.4.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `agenda1`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `citas`
--

CREATE TABLE `citas` (
  `cit_id` int(11) NOT NULL COMMENT 'identificador de la cita',
  `con_id` int(11) NOT NULL COMMENT 'identificador del contacto',
  `cit_lugar` text NOT NULL COMMENT 'lugar de la cita',
  `cit_fecha` date NOT NULL COMMENT 'fecha de la cita',
  `cit_hora` time NOT NULL COMMENT 'hora de la cita',
  `cit_descripcion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='tabla de las citas con los contactos';

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `contactos`
--

CREATE TABLE `contactos` (
  `con_id` int(11) NOT NULL COMMENT 'identificador del contacto',
  `user_id` int(11) NOT NULL COMMENT 'identificador de usuario',
  `con_nombre` varchar(50) NOT NULL COMMENT 'nombre del contacto',
  `con_apellido` varchar(50) NOT NULL COMMENT 'apellido del contacto',
  `con_direccion` varchar(250) NOT NULL COMMENT 'dirección del contacto',
  `con_telefono` varchar(20) NOT NULL COMMENT 'teléfono del contacto',
  `con_email` varchar(25) NOT NULL COMMENT 'correo electrónico del contacto'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='tabla de los contactos de la agenda';

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `user_id` int(11) NOT NULL COMMENT 'identificador del usuario',
  `user_name` varchar(45) NOT NULL COMMENT 'nombre del usuario',
  `user_password` varchar(45) NOT NULL COMMENT 'contraseña del usuario'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
  ADD KEY `fk_usuario_contacto` (`user_id`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `citas`
--
ALTER TABLE `citas`
  MODIFY `cit_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'identificador de la cita', AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `contactos`
--
ALTER TABLE `contactos`
  MODIFY `con_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'identificador del contacto', AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'identificador del usuario';

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `citas`
--
ALTER TABLE `citas`
  ADD CONSTRAINT `fk_citas_contactos` FOREIGN KEY (`con_id`) REFERENCES `contactos` (`con_id`);

--
-- Filtros para la tabla `contactos`
--
ALTER TABLE `contactos`
  ADD CONSTRAINT `fk_usuario_contacto` FOREIGN KEY (`user_id`) REFERENCES `usuario` (`user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

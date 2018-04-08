DROP DATABASE IF EXISTS `echart`;

CREATE DATABASE IF NOT EXISTS `echart` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `echart`;

CREATE TABLE `spider` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `insert_time` text NOT NULL,
  `num` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

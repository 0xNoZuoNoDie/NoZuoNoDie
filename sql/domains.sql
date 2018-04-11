
USE `Domain`;

CREATE TABLE `domains` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domin` int(11) NOT NULL,
  `cms_id` int(11) DEFAULT NULL,
  `ip_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

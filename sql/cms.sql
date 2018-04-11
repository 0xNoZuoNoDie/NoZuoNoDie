USE `Domain`;

CREATE TABLE `cms` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cms` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO cms (cms) VALUES ('Discuz'), ('EmpireCMS'), ('Phpyun'), ('DESTOONB2B'), ('PHPWind'), ('phpcms'), ('metinfo');

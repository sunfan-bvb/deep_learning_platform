/*
 Navicat Premium Data Transfer

 Source Server         : root
 Source Server Type    : MySQL
 Source Server Version : 80028
 Source Host           : localhost:3306
 Source Schema         : deepL

 Target Server Type    : MySQL
 Target Server Version : 80028
 File Encoding         : 65001

 Date: 16/04/2022 12:03:07
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for project
-- ----------------------------
DROP TABLE IF EXISTS `project`;
CREATE TABLE `project` (
  `user` varchar(255) NOT NULL,
  `project` varchar(255) NOT NULL,
  `date` varchar(255) NOT NULL,
  `type` varchar(255) NOT NULL,
  PRIMARY KEY (`user`,`project`,`type`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of project
-- ----------------------------
BEGIN;
INSERT INTO `project` (`user`, `project`, `date`, `type`) VALUES ('Bob', 'fea', '2022-4-13', 'visual');
INSERT INTO `project` (`user`, `project`, `date`, `type`) VALUES ('Bob', 'fea1', '2022-4-13', 'visual');
INSERT INTO `project` (`user`, `project`, `date`, `type`) VALUES ('Bob', 'node', '2022-4-14', 'visual');
INSERT INTO `project` (`user`, `project`, `date`, `type`) VALUES ('Bob', 'torch', '2022-4-13', 'code');
INSERT INTO `project` (`user`, `project`, `date`, `type`) VALUES ('Sam', 'bbbb', '2022-2-11', 'visual');
INSERT INTO `project` (`user`, `project`, `date`, `type`) VALUES ('Sam', 'code1', '2022-3-12', 'code');
INSERT INTO `project` (`user`, `project`, `date`, `type`) VALUES ('Sam', 'val', '2022-3-23', 'visual');
INSERT INTO `project` (`user`, `project`, `date`, `type`) VALUES ('Sam', 'visual_test', '2022-4-12', 'visual');
INSERT INTO `project` (`user`, `project`, `date`, `type`) VALUES ('Sam', '未命名', '2022-3-28', 'code');
INSERT INTO `project` (`user`, `project`, `date`, `type`) VALUES ('Sam', '未命名', '2022-2-19', 'visual');
COMMIT;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of user
-- ----------------------------
BEGIN;
INSERT INTO `user` (`id`, `name`, `password`) VALUES (1, 'Sam', '601f1889667efaebb33b8c12572835da3f027f78');
INSERT INTO `user` (`id`, `name`, `password`) VALUES (2, 'Amy', '601f1889667efaebb33b8c12572835da3f027f78');
INSERT INTO `user` (`id`, `name`, `password`) VALUES (12, 'Bob', '601f1889667efaebb33b8c12572835da3f027f78');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;

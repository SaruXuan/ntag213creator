-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2020-06-11 09:22:51
-- 伺服器版本： 10.4.11-MariaDB
-- PHP 版本： 7.4.5

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `amiibo`
--
CREATE DATABASE IF NOT EXISTS `amiibo` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `amiibo`;

-- --------------------------------------------------------

--
-- 資料表結構 `available`
--

CREATE TABLE `available` (
  `GAME_ID` int(10) UNSIGNED NOT NULL,
  `TREASURE_ID` int(10) UNSIGNED NOT NULL,
  `AVAILABILITY` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 傾印資料表的資料 `available`
--

INSERT INTO `available` (`GAME_ID`, `TREASURE_ID`, `AVAILABILITY`) VALUES
(1, 1, 1),
(1, 2, 1),
(1, 3, 1),
(1, 4, 1),
(1, 5, 1),
(1, 6, 1),
(1, 7, 1),
(1, 8, 1),
(1, 9, 1);

-- --------------------------------------------------------

--
-- 資料表結構 `game`
--

CREATE TABLE `game` (
  `GAME_ID` int(10) UNSIGNED NOT NULL,
  `RELEASE_DATE` date DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 傾印資料表的資料 `game`
--

INSERT INTO `game` (`GAME_ID`, `RELEASE_DATE`) VALUES
(1, '2020-03-20');

-- --------------------------------------------------------

--
-- 資料表結構 `game_name`
--

CREATE TABLE `game_name` (
  `GAME_ID` int(10) UNSIGNED NOT NULL,
  `LANGUAGE_ID` int(10) UNSIGNED NOT NULL,
  `GNAME` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 傾印資料表的資料 `game_name`
--

INSERT INTO `game_name` (`GAME_ID`, `LANGUAGE_ID`, `GNAME`) VALUES
(1, 1, 'Animal Crossing'),
(1, 2, '動物森友會'),
(1, 3, 'どうぶつの森');

-- --------------------------------------------------------

--
-- 資料表結構 `language`
--

CREATE TABLE `language` (
  `LANGUAGE_ID` int(10) UNSIGNED NOT NULL,
  `LNAME` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 傾印資料表的資料 `language`
--

INSERT INTO `language` (`LANGUAGE_ID`, `LNAME`) VALUES
(1, 'english'),
(2, 'tchinese'),
(3, 'japanese');

-- --------------------------------------------------------

--
-- 資料表結構 `treasure`
--

CREATE TABLE `treasure` (
  `TREASURE_ID` int(10) UNSIGNED NOT NULL,
  `TREASURE_KEY` char(16) COLLATE utf8mb4_unicode_ci NOT NULL,
  `IMAGE_URL` varchar(10000) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '/imgs/Empty.jpg'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 傾印資料表的資料 `treasure`
--

INSERT INTO `treasure` (`TREASURE_ID`, `TREASURE_KEY`, `IMAGE_URL`) VALUES
(1, 'jC0Vln1y5je9BiZk', '/imgs/001 ISABELLE.png'),
(2, 'j4snTqKCYLjXoxBP', '/imgs/002 TOM NOOK.png'),
(3, 'by6ZDrSjW4I4MDTU', '/imgs/034 KIKI.png'),
(4, 'IaAOILuwtIFvA0QJ', '/imgs/037 KABUKI.png'),
(5, 'mitHeGervlo4z395', '/imgs/107 KATIE.png'),
(6, 'YHXcd3KDw1Cjt6dn', '/imgs/188 ANKHA.png'),
(7, '7nfpikt1KfoL2Grt', '/imgs/264 MARSHAL.png'),
(8, 'ii5ulafmeNrQrSfE', '/imgs/294 MAPLE.png'),
(9, 'MXuqqKwk1BYfxJLd', '/imgs/357 AURORA.png');

-- --------------------------------------------------------

--
-- 資料表結構 `treasure_name`
--

CREATE TABLE `treasure_name` (
  `LANGUAGE_ID` int(10) UNSIGNED NOT NULL,
  `TREASURE_ID` int(10) UNSIGNED NOT NULL,
  `NAME` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 傾印資料表的資料 `treasure_name`
--

INSERT INTO `treasure_name` (`LANGUAGE_ID`, `TREASURE_ID`, `NAME`) VALUES
(1, 1, 'Isabelle'),
(1, 2, 'Tom Nook'),
(1, 3, 'Kiki'),
(1, 4, 'Kabuki'),
(1, 5, 'Katie'),
(1, 6, 'Ankha'),
(1, 7, 'Marshal'),
(1, 8, 'Maple'),
(1, 9, 'Aurora'),
(2, 1, '西施惠'),
(2, 2, '狸克'),
(2, 3, '余子醬'),
(2, 4, '戈伍紀'),
(2, 5, '咪露'),
(2, 6, '艷后'),
(2, 7, '小潤'),
(2, 8, '小楓'),
(2, 9, '歐若拉'),
(3, 1, 'しずえ'),
(3, 2, 'たぬきち'),
(3, 3, 'キャビア'),
(3, 4, 'かぶきち'),
(3, 5, 'まいこちゃん'),
(3, 6, 'ナイル'),
(3, 7, 'ジュン'),
(3, 8, 'メープル'),
(3, 9, 'オーロラ');

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `available`
--
ALTER TABLE `available`
  ADD PRIMARY KEY (`GAME_ID`,`TREASURE_ID`),
  ADD KEY `TREASURE_ID` (`TREASURE_ID`);

--
-- 資料表索引 `game`
--
ALTER TABLE `game`
  ADD PRIMARY KEY (`GAME_ID`);

--
-- 資料表索引 `game_name`
--
ALTER TABLE `game_name`
  ADD PRIMARY KEY (`GAME_ID`,`LANGUAGE_ID`),
  ADD KEY `LANGUAGE_ID` (`LANGUAGE_ID`);

--
-- 資料表索引 `language`
--
ALTER TABLE `language`
  ADD PRIMARY KEY (`LANGUAGE_ID`);

--
-- 資料表索引 `treasure`
--
ALTER TABLE `treasure`
  ADD PRIMARY KEY (`TREASURE_ID`);

--
-- 資料表索引 `treasure_name`
--
ALTER TABLE `treasure_name`
  ADD PRIMARY KEY (`LANGUAGE_ID`,`TREASURE_ID`),
  ADD KEY `TREASURE_ID` (`TREASURE_ID`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `game`
--
ALTER TABLE `game`
  MODIFY `GAME_ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `language`
--
ALTER TABLE `language`
  MODIFY `LANGUAGE_ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `treasure`
--
ALTER TABLE `treasure`
  MODIFY `TREASURE_ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- 已傾印資料表的限制式
--

--
-- 資料表的限制式 `available`
--
ALTER TABLE `available`
  ADD CONSTRAINT `available_ibfk_1` FOREIGN KEY (`GAME_ID`) REFERENCES `game` (`GAME_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `available_ibfk_2` FOREIGN KEY (`TREASURE_ID`) REFERENCES `treasure` (`TREASURE_ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- 資料表的限制式 `game_name`
--
ALTER TABLE `game_name`
  ADD CONSTRAINT `game_name_ibfk_1` FOREIGN KEY (`GAME_ID`) REFERENCES `game` (`GAME_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `game_name_ibfk_2` FOREIGN KEY (`LANGUAGE_ID`) REFERENCES `language` (`LANGUAGE_ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- 資料表的限制式 `treasure_name`
--
ALTER TABLE `treasure_name`
  ADD CONSTRAINT `treasure_name_ibfk_1` FOREIGN KEY (`LANGUAGE_ID`) REFERENCES `language` (`LANGUAGE_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `treasure_name_ibfk_2` FOREIGN KEY (`TREASURE_ID`) REFERENCES `treasure` (`TREASURE_ID`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

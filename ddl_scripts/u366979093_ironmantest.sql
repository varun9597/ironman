-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 14, 2024 at 03:41 AM
-- Server version: 10.11.7-MariaDB-cll-lve
-- PHP Version: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `u366979093_ironmantest`
--

-- --------------------------------------------------------

--
-- Table structure for table `tbl_customer`
--

CREATE TABLE `tbl_customer` (
  `pk_cust_id` int(11) NOT NULL,
  `cust_name` varchar(255) NOT NULL,
  `fk_soc_id` int(11) DEFAULT NULL,
  `cust_phone` varchar(15) NOT NULL,
  `fk_user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_cust_flat`
--

CREATE TABLE `tbl_cust_flat` (
  `pk_flat_id` int(11) NOT NULL,
  `flat_no` varchar(20) NOT NULL,
  `fk_cust_id` int(11) DEFAULT NULL,
  `fk_soc_id` int(11) DEFAULT NULL,
  `fk_user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_items`
--

CREATE TABLE `tbl_items` (
  `pk_item_id` int(11) NOT NULL,
  `item_name` varchar(255) NOT NULL,
  `fk_user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_orders`
--

CREATE TABLE `tbl_orders` (
  `pk_order_id` int(11) NOT NULL,
  `fk_cust_id` int(11) NOT NULL,
  `fk_user_id` int(11) NOT NULL,
  `order_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `total_amt` decimal(10,2) NOT NULL DEFAULT 0.00,
  `bill_status` varchar(20) NOT NULL DEFAULT 'Not Paid'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_order_items`
--

CREATE TABLE `tbl_order_items` (
  `pk_order_item_id` int(11) NOT NULL,
  `fk_order_id` int(11) DEFAULT NULL,
  `fk_item_id` int(11) DEFAULT NULL,
  `quantity` int(11) NOT NULL DEFAULT 0,
  `price` decimal(10,2) NOT NULL DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_rate_card`
--

CREATE TABLE `tbl_rate_card` (
  `pk_rate_id` int(11) NOT NULL,
  `fk_item_id` int(11) DEFAULT NULL,
  `fk_user_id` int(11) DEFAULT NULL,
  `fk_soc_id` int(11) DEFAULT NULL,
  `rate` decimal(5,1) DEFAULT 0.0,
  `insert_date` datetime NOT NULL DEFAULT current_timestamp(),
  `update_date` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_society`
--

CREATE TABLE `tbl_society` (
  `pk_soc_id` int(11) NOT NULL,
  `soc_name` varchar(255) NOT NULL,
  `fk_user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_users`
--

CREATE TABLE `tbl_users` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tbl_customer`
--
ALTER TABLE `tbl_customer`
  ADD PRIMARY KEY (`pk_cust_id`),
  ADD KEY `fk_soc_id` (`fk_soc_id`),
  ADD KEY `fk_user_id` (`fk_user_id`);

--
-- Indexes for table `tbl_cust_flat`
--
ALTER TABLE `tbl_cust_flat`
  ADD PRIMARY KEY (`pk_flat_id`),
  ADD KEY `fk_cust_id` (`fk_cust_id`),
  ADD KEY `fk_soc_id` (`fk_soc_id`),
  ADD KEY `fk_user_id` (`fk_user_id`);

--
-- Indexes for table `tbl_items`
--
ALTER TABLE `tbl_items`
  ADD PRIMARY KEY (`pk_item_id`);

--
-- Indexes for table `tbl_orders`
--
ALTER TABLE `tbl_orders`
  ADD PRIMARY KEY (`pk_order_id`),
  ADD KEY `fk_cust_id` (`fk_cust_id`),
  ADD KEY `fk_user_id` (`fk_user_id`);

--
-- Indexes for table `tbl_order_items`
--
ALTER TABLE `tbl_order_items`
  ADD PRIMARY KEY (`pk_order_item_id`),
  ADD KEY `fk_order_id` (`fk_order_id`),
  ADD KEY `fk_item_id` (`fk_item_id`);

--
-- Indexes for table `tbl_rate_card`
--
ALTER TABLE `tbl_rate_card`
  ADD PRIMARY KEY (`pk_rate_id`),
  ADD KEY `fk_user_id` (`fk_user_id`),
  ADD KEY `fk_soc_id` (`fk_soc_id`),
  ADD KEY `tbl_rate_card_ibfk_1` (`fk_item_id`);

--
-- Indexes for table `tbl_society`
--
ALTER TABLE `tbl_society`
  ADD PRIMARY KEY (`pk_soc_id`),
  ADD KEY `fk_user` (`fk_user_id`);

--
-- Indexes for table `tbl_users`
--
ALTER TABLE `tbl_users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tbl_customer`
--
ALTER TABLE `tbl_customer`
  MODIFY `pk_cust_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_cust_flat`
--
ALTER TABLE `tbl_cust_flat`
  MODIFY `pk_flat_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_items`
--
ALTER TABLE `tbl_items`
  MODIFY `pk_item_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_orders`
--
ALTER TABLE `tbl_orders`
  MODIFY `pk_order_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_order_items`
--
ALTER TABLE `tbl_order_items`
  MODIFY `pk_order_item_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_rate_card`
--
ALTER TABLE `tbl_rate_card`
  MODIFY `pk_rate_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_society`
--
ALTER TABLE `tbl_society`
  MODIFY `pk_soc_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_users`
--
ALTER TABLE `tbl_users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `tbl_customer`
--
ALTER TABLE `tbl_customer`
  ADD CONSTRAINT `tbl_customer_ibfk_1` FOREIGN KEY (`fk_soc_id`) REFERENCES `tbl_society` (`pk_soc_id`),
  ADD CONSTRAINT `tbl_customer_ibfk_2` FOREIGN KEY (`fk_user_id`) REFERENCES `tbl_users` (`id`);

--
-- Constraints for table `tbl_cust_flat`
--
ALTER TABLE `tbl_cust_flat`
  ADD CONSTRAINT `tbl_cust_flat_ibfk_1` FOREIGN KEY (`fk_cust_id`) REFERENCES `tbl_customer` (`pk_cust_id`),
  ADD CONSTRAINT `tbl_cust_flat_ibfk_2` FOREIGN KEY (`fk_soc_id`) REFERENCES `tbl_society` (`pk_soc_id`),
  ADD CONSTRAINT `tbl_cust_flat_ibfk_3` FOREIGN KEY (`fk_user_id`) REFERENCES `tbl_users` (`id`);

--
-- Constraints for table `tbl_orders`
--
ALTER TABLE `tbl_orders`
  ADD CONSTRAINT `fk_orders_customer` FOREIGN KEY (`fk_cust_id`) REFERENCES `tbl_customer` (`pk_cust_id`),
  ADD CONSTRAINT `fk_orders_users` FOREIGN KEY (`fk_user_id`) REFERENCES `tbl_users` (`id`);

--
-- Constraints for table `tbl_order_items`
--
ALTER TABLE `tbl_order_items`
  ADD CONSTRAINT `tbl_order_items_ibfk_1` FOREIGN KEY (`fk_order_id`) REFERENCES `tbl_orders` (`pk_order_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `tbl_order_items_ibfk_2` FOREIGN KEY (`fk_item_id`) REFERENCES `tbl_items` (`pk_item_id`);

--
-- Constraints for table `tbl_rate_card`
--
ALTER TABLE `tbl_rate_card`
  ADD CONSTRAINT `tbl_rate_card_ibfk_1` FOREIGN KEY (`fk_item_id`) REFERENCES `tbl_items` (`pk_item_id`),
  ADD CONSTRAINT `tbl_rate_card_ibfk_2` FOREIGN KEY (`fk_user_id`) REFERENCES `tbl_users` (`id`),
  ADD CONSTRAINT `tbl_rate_card_ibfk_3` FOREIGN KEY (`fk_soc_id`) REFERENCES `tbl_society` (`pk_soc_id`);

--
-- Constraints for table `tbl_society`
--
ALTER TABLE `tbl_society`
  ADD CONSTRAINT `fk_user` FOREIGN KEY (`fk_user_id`) REFERENCES `tbl_users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

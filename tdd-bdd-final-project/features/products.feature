Feature: Product management
  As a product manager
  I want to manage products
  So that I can maintain the product catalogue

  Background:
    Given the product service is running

  Scenario: Create and read a product
    When I create a product named "Notebook"
    Then the product should be available in the catalogue

package com.ssafy.javer.Service;

import java.util.List;	

import com.ssafy.javer.DTO.News_dto;
import com.ssafy.javer.DTO.Stock_dto;

public interface StockService {
	public List<Stock_dto> SelectListStock();
}

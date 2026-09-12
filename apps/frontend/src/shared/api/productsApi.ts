import { createApi } from '@reduxjs/toolkit/query/react';
import { baseQuery } from './api';
import type { ProductDetails, ProductListItem, ProductQueryParams } from '../types/products';

export const productsApi = createApi({
  reducerPath: 'productsApi',
  baseQuery,
  endpoints: (builder) => ({
    getProducts: builder.query<ProductListItem[], ProductQueryParams | undefined>({
      query: (params) => ({
        url: 'products/',
        params: {
          lang: params?.lang,
          currency: params?.currency,
        },
      }),
    }),
    getProductById: builder.query<ProductDetails, { id: number } & ProductQueryParams>({
      query: ({ id, lang, currency }) => ({
        url: `products/${id}/`,
        params: { lang, currency },
      }),
    }),
  }),
});

export const { useGetProductsQuery, useGetProductByIdQuery } = productsApi;
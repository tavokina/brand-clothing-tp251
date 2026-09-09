import type { User } from './User';
import type { CartItem } from './CartItem';


export type Cart = {
  id: number;
  user: User;
  session: string;
  items: CartItem[];
  created_at: string;
  updated_at: string;
}
/**
 * NextAuth.js Configuration
 * OAuth providers: Google, Facebook, Email/Password
 */
import { NextAuthOptions } from 'next-auth';
import GoogleProvider from 'next-auth/providers/google';
import FacebookProvider from 'next-auth/providers/facebook';
import CredentialsProvider from 'next-auth/providers/credentials';
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const authOptions: NextAuthOptions = {
  providers: [
    // Google OAuth Provider
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID || '',
      clientSecret: process.env.GOOGLE_CLIENT_SECRET || '',
      authorization: {
        params: {
          prompt: 'consent',
          access_type: 'offline',
          response_type: 'code'
        }
      }
    }),

    // Facebook OAuth Provider
    FacebookProvider({
      clientId: process.env.FACEBOOK_CLIENT_ID || '',
      clientSecret: process.env.FACEBOOK_CLIENT_SECRET || ''
    }),

    // Email/Password Credentials Provider
    CredentialsProvider({
      name: 'Credentials',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' }
      },
      async authorize(credentials) {
        try {
          if (!credentials?.email || !credentials?.password) {
            return null;
          }

          // Authenticate with backend
          const response = await axios.post(`${API_BASE_URL}/api/v1/auth/login`, {
            email: credentials.email,
            password: credentials.password
          });

          if (response.data && response.data.access_token) {
            return {
              id: response.data.user_id,
              email: credentials.email,
              accessToken: response.data.access_token
            };
          }

          return null;
        } catch (error) {
          console.error('Authentication error:', error);
          return null;
        }
      }
    })
  ],

  callbacks: {
    async jwt({ token, user, account }) {
      // Initial sign in
      if (account && user) {
        // For OAuth providers
        if (account.provider === 'google' || account.provider === 'facebook') {
          try {
            // Send OAuth token to backend for verification
            const response = await axios.post(`${API_BASE_URL}/api/v1/auth/oauth`, {
              provider: account.provider,
              access_token: account.access_token,
              id_token: account.id_token,
              email: user.email,
              name: user.name
            });

            token.accessToken = response.data.access_token;
            token.userId = response.data.user_id;
          } catch (error) {
            console.error('OAuth backend verification failed:', error);
          }
        } else {
          // For credentials provider
          token.accessToken = (user as any).accessToken;
          token.userId = user.id;
        }
      }

      return token;
    },

    async session({ session, token }) {
      // Add custom fields to session
      if (token) {
        (session as any).accessToken = token.accessToken;
        (session as any).userId = token.userId;
      }
      return session;
    }
  },

  pages: {
    signIn: '/login',
    error: '/login'
  },

  session: {
    strategy: 'jwt',
    maxAge: 30 * 24 * 60 * 60 // 30 days
  },

  secret: process.env.NEXTAUTH_SECRET
};

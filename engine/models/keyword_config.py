"""
engine/models/keyword_config.py

Central fraud keyword configuration for the NovaMind Retail Risk Agent.

This module contains immutable keyword categories used by the RuleEngine
to perform deterministic fraud signal extraction.

Responsibilities
----------------
- Define fraud-related keyword vocabularies.
- Provide a centralized registry of keyword categories.
- Remain free of business logic and NLP processing.

Notes
-----
- All keyword collections are immutable (frozenset).
- RuleEngine should iterate over KEYWORD_CATEGORIES rather than
  importing individual category constants.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet


# ==========================================================
# DATA MODEL
# ==========================================================


@dataclass(frozen=True, slots=True)
class KeywordCategory:
    """
    Immutable fraud keyword category.

    Attributes
    ----------
    name:
        Unique category identifier.

    description:
        Human-readable explanation.

    keywords:
        Fraud-related vocabulary belonging to this category.
    """

    name: str
    description: str
    keywords: FrozenSet[str]


# ==========================================================
# CATEGORY DEFINITIONS
# ==========================================================


URGENCY = KeywordCategory(
    name="urgency",
    description="Pressure tactics encouraging immediate action.",
    keywords=frozenset({
        "act now",
        "asap",
        "at once",
        "critical",
        "don't delay",
        "emergency",
        "expire",
        "expires today",
        "hurry",
        "immediate",
        "immediately",
        "instant",
        "last chance",
        "now",
        "right away",
        "time sensitive",
        "today",
        "urgent",
        "warning",
        "within minutes",
    }),
)


PAYMENT = KeywordCategory(
    name="payment",
    description="General payment and transaction terminology.",
    keywords=frozenset({
        "amount",
        "bank transfer",
        "bill",
        "card payment",
        "cash",
        "credit",
        "debit",
        "deposit",
        "invoice",
        "money",
        "pay",
        "payment",
        "purchase",
        "receive payment",
        "send money",
        "transaction",
        "transfer",
        "upi",
        "wallet",
        "wire transfer",
    }),
)


REFUND = KeywordCategory(
    name="refund",
    description="Refund and reimbursement related language.",
    keywords=frozenset({
        "cancel order",
        "chargeback",
        "claim",
        "compensation",
        "credit back",
        "money back",
        "refund",
        "refund approved",
        "refund pending",
        "refund request",
        "refund status",
        "replacement",
        "reversal",
        "return",
        "returned",
        "returned item",
        "reimburse",
        "reimbursement",
        "reverse payment",
        "store credit",
    }),
)


BANKING = KeywordCategory(
    name="banking",
    description="Banking terminology and financial institutions.",
    keywords=frozenset({
        "account balance",
        "bank",
        "bank account",
        "bank branch",
        "beneficiary",
        "card",
        "checking account",
        "current account",
        "debit card",
        "financial institution",
        "iban",
        "ifsc",
        "net banking",
        "routing number",
        "savings account",
        "swift",
        "swift code",
        "virtual account",
        "withdraw",
        "withdrawal",
    }),
)


ACCOUNT = KeywordCategory(
    name="account",
    description="User account and profile terminology.",
    keywords=frozenset({
        "account",
        "account blocked",
        "account details",
        "account locked",
        "account suspended",
        "activate account",
        "close account",
        "customer id",
        "dashboard",
        "login",
        "logout",
        "profile",
        "profile update",
        "reactivate",
        "register",
        "sign in",
        "sign up",
        "unlock account",
        "user account",
        "username",
    }),
)


AUTHENTICATION = KeywordCategory(
    name="authentication",
    description="Authentication and identity verification terms.",
    keywords=frozenset({
        "2fa",
        "authenticate",
        "authentication",
        "authorization",
        "confirm identity",
        "login verification",
        "mfa",
        "one time password",
        "otp",
        "passcode",
        "password",
        "pin",
        "security code",
        "token",
        "two factor authentication",
        "verification",
        "verification code",
        "verify",
        "verify identity",
        "verify login",
    }),
)


SECURITY = KeywordCategory(
    name="security",
    description="Security warnings and suspicious activity.",
    keywords=frozenset({
        "alert",
        "breach",
        "compromised",
        "credential",
        "cyber attack",
        "fraud",
        "hack",
        "hacked",
        "malware",
        "risk",
        "safe",
        "secure",
        "security",
        "security alert",
        "security check",
        "suspicious",
        "threat",
        "unauthorized",
        "unsafe",
        "virus",
    }),
)


IDENTITY = KeywordCategory(
    name="identity",
    description="Identity verification and personal information.",
    keywords=frozenset({
        "aadhaar",
        "address proof",
        "date of birth",
        "dl",
        "driving licence",
        "identity",
        "identity proof",
        "id",
        "id card",
        "kyc",
        "name",
        "national id",
        "pan",
        "passport",
        "photo id",
        "personal details",
        "ssn",
        "tax id",
        "verify identity",
        "voter id",
    }),
)


IMPERSONATION = KeywordCategory(
    name="impersonation",
    description="Authority or support impersonation attempts.",
    keywords=frozenset({
        "bank executive",
        "bank officer",
        "customer care",
        "customer support",
        "executive",
        "government official",
        "help desk",
        "manager",
        "official",
        "police",
        "representative",
        "reserve bank",
        "rbi",
        "service agent",
        "support team",
        "technical executive",
        "verified agent",
        "verification officer",
        "your bank",
        "your provider",
    }),
)

PHISHING = KeywordCategory(
    name="phishing",
    description="Credential theft and phishing terminology.",
    keywords=frozenset({
        "account verification",
        "click here",
        "confirm account",
        "confirm password",
        "email verification",
        "fake website",
        "login page",
        "malicious link",
        "open attachment",
        "phishing",
        "reset password",
        "secure your account",
        "sign in here",
        "sms verification",
        "suspicious email",
        "update account",
        "verify email",
        "verify password",
        "web link",
        "your account is at risk",
    }),
)


GIFT_CARD = KeywordCategory(
    name="gift_card",
    description="Gift card fraud terminology.",
    keywords=frozenset({
        "amazon gift card",
        "apple gift card",
        "buy gift card",
        "gift card",
        "gift voucher",
        "google play card",
        "itunes card",
        "load balance",
        "prepaid card",
        "redeem",
        "redeem code",
        "redemption",
        "scratch code",
        "steam card",
        "top up",
        "voucher",
        "voucher code",
        "wallet code",
        "xbox card",
        "gift coupon",
    }),
)


CRYPTOCURRENCY = KeywordCategory(
    name="cryptocurrency",
    description="Cryptocurrency and blockchain terminology.",
    keywords=frozenset({
        "binance",
        "bitcoin",
        "blockchain",
        "bnb",
        "btc",
        "coinbase",
        "crypto",
        "cryptocurrency",
        "ethereum",
        "eth",
        "exchange wallet",
        "ledger",
        "metamask",
        "private key",
        "seed phrase",
        "token",
        "trx",
        "usdc",
        "usdt",
        "wallet address",
    }),
)


DELIVERY = KeywordCategory(
    name="delivery",
    description="Delivery and shipping related terminology.",
    keywords=frozenset({
        "address confirmation",
        "courier",
        "delayed shipment",
        "delivery",
        "delivery attempt",
        "dispatch",
        "logistics",
        "order shipped",
        "package",
        "parcel",
        "pickup",
        "shipment",
        "shipping",
        "shipping fee",
        "tracking",
        "tracking id",
        "tracking number",
        "warehouse",
        "waybill",
        "wrong address",
    }),
)


PROMOTION = KeywordCategory(
    name="promotion",
    description="Discount and promotional offer terminology.",
    keywords=frozenset({
        "bonus",
        "cashback",
        "claim reward",
        "coupon",
        "discount",
        "exclusive offer",
        "free gift",
        "limited offer",
        "offer",
        "promo",
        "promo code",
        "promotion",
        "redeem reward",
        "reward",
        "sale",
        "special offer",
        "unlock reward",
        "voucher",
        "win prize",
        "winner",
    }),
)


LOYALTY = KeywordCategory(
    name="loyalty",
    description="Loyalty and reward program terminology.",
    keywords=frozenset({
        "bonus points",
        "earn points",
        "loyal customer",
        "loyalty",
        "loyalty account",
        "membership",
        "points",
        "premium member",
        "redeem points",
        "reward balance",
        "reward credits",
        "reward points",
        "rewards",
        "status level",
        "tier",
        "upgrade membership",
        "vip",
        "vip customer",
        "wallet points",
        "welcome bonus",
    }),
)


LEGAL = KeywordCategory(
    name="legal",
    description="Legal threats and compliance terminology.",
    keywords=frozenset({
        "arrest",
        "case",
        "complaint",
        "court",
        "criminal",
        "fine",
        "fraud investigation",
        "government notice",
        "law enforcement",
        "legal",
        "legal action",
        "legal notice",
        "lawsuit",
        "non compliance",
        "notice",
        "penalty",
        "police complaint",
        "prosecution",
        "summons",
        "warrant",
    }),
)


TECHNICAL_SUPPORT = KeywordCategory(
    name="technical_support",
    description="Technical support scam terminology.",
    keywords=frozenset({
        "access your device",
        "anydesk",
        "customer support",
        "desktop sharing",
        "install software",
        "it support",
        "quicksupport",
        "remote access",
        "remote desktop",
        "screen share",
        "support agent",
        "support engineer",
        "support session",
        "teamviewer",
        "technical issue",
        "technical support",
        "troubleshoot",
        "ultraviewer",
        "update software",
        "windows support",
    }),
)


SOCIAL_ENGINEERING = KeywordCategory(
    name="social_engineering",
    description="Manipulation and psychological pressure tactics.",
    keywords=frozenset({
        "act immediately",
        "assist me",
        "confidential",
        "do not tell anyone",
        "don't inform anyone",
        "emergency help",
        "family emergency",
        "help urgently",
        "keep secret",
        "only you",
        "private request",
        "secret",
        "special request",
        "strictly confidential",
        "trust me",
        "urgent assistance",
        "verify immediately",
        "you are selected",
        "your cooperation",
        "your help",
    }),
)


# ==========================================================
# COMPLETE REGISTRY
# ==========================================================

KEYWORD_CATEGORIES: dict[str, KeywordCategory] = {
    URGENCY.name: URGENCY,
    PAYMENT.name: PAYMENT,
    REFUND.name: REFUND,
    BANKING.name: BANKING,
    ACCOUNT.name: ACCOUNT,
    AUTHENTICATION.name: AUTHENTICATION,
    SECURITY.name: SECURITY,
    IDENTITY.name: IDENTITY,
    IMPERSONATION.name: IMPERSONATION,
    PHISHING.name: PHISHING,
    GIFT_CARD.name: GIFT_CARD,
    CRYPTOCURRENCY.name: CRYPTOCURRENCY,
    DELIVERY.name: DELIVERY,
    PROMOTION.name: PROMOTION,
    LOYALTY.name: LOYALTY,
    LEGAL.name: LEGAL,
    TECHNICAL_SUPPORT.name: TECHNICAL_SUPPORT,
    SOCIAL_ENGINEERING.name: SOCIAL_ENGINEERING,
}


# ==========================================================
# PUBLIC API
# ==========================================================

__all__ = [
    "KeywordCategory",
    "KEYWORD_CATEGORIES",
]